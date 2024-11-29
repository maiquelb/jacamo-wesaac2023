import pygame
import math
from simulation.config import SimConfig

class Visualizer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.detection_flash_duration = 30  # frames
        self.detection_flashes = {}  # {uav_id: frames_remaining}

        # Initialize statistics
        self.active_uavs = []
        self.active_boats = []
        self.victims_found = 0
        self.victims_rescued = 0
        self.total_victims = 0

    def draw_all(self, uavs, boats, victims, communication):
        # Clear screen
        self.screen.fill((255, 255, 255))  # White background

        # Update statistics before drawing
        self.update_stats(uavs, boats, victims)

        # Draw regions
        self.draw_regions()
        self.draw_stations_with_agents(uavs, boats)
        self.draw_rescue_area(uavs, boats, victims)
        self.draw_legend()

        # Draw UAVs with detection feedback
        for uav in uavs:
            # Draw detection radius
            if uav.state == "MONITORING":
                pygame.draw.circle(self.screen, (0, 255, 0, 50),
                                 (int(uav.position.x), int(uav.position.y)),
                                 uav.detection_radius, 1)

            # Draw UAV with flashing effect if detecting
            if uav.id in self.detection_flashes and self.detection_flashes[uav.id] > 0:
                # Flash between green and yellow
                color = (255, 255, 0) if self.detection_flashes[uav.id] % 10 < 5 else SimConfig.UAV_COLOR
                self.detection_flashes[uav.id] -= 1
            else:
                color = SimConfig.UAV_COLOR

            pygame.draw.circle(self.screen, color,
                             (int(uav.position.x), int(uav.position.y)), 7)

            # Draw line to victim being followed
            if uav.following_victim:
                pygame.draw.line(self.screen, (255, 255, 0),
                               (int(uav.position.x), int(uav.position.y)),
                               (int(uav.following_victim.position.x),
                                int(uav.following_victim.position.y)), 1)

    def draw_regions(self):
        """Draw the three main regions"""
        # Station region (left)
        pygame.draw.rect(self.screen, SimConfig.REGION_BORDER,
                        (0, 0, SimConfig.STATION_REGION_WIDTH, SimConfig.WINDOW_SIZE[1]), 2)

        # Rescue region (middle)
        rescue_region_x = SimConfig.STATION_REGION_WIDTH
        pygame.draw.rect(self.screen, SimConfig.REGION_BORDER,
                        (rescue_region_x, 0, SimConfig.RESCUE_REGION_WIDTH, SimConfig.WINDOW_SIZE[1]), 2)

        # Legend region (right)
        legend_region_x = SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_WIDTH
        pygame.draw.rect(self.screen, SimConfig.REGION_BORDER,
                        (legend_region_x, 0, SimConfig.LEGEND_REGION_WIDTH, SimConfig.WINDOW_SIZE[1]), 2)

    def draw_stations_with_agents(self, uavs, boats):
        """Draw stations with their assigned agents"""
        available_height = SimConfig.WINDOW_SIZE[1] - SimConfig.STATION_TOP_MARGIN * 2
        total_station_space = (SimConfig.STATION_HEIGHT + SimConfig.STATION_MARGIN) * 5

        # Calculate starting Y position to center stations vertically
        start_y = (SimConfig.WINDOW_SIZE[1] - total_station_space) // 2

        for i in range(5):  # 5 stations
            station_y = start_y + i * (SimConfig.STATION_HEIGHT + SimConfig.STATION_MARGIN)

            # Draw station rectangle
            station_rect = pygame.Rect(
                SimConfig.STATION_MARGIN,
                station_y,
                SimConfig.STATION_WIDTH,
                SimConfig.STATION_HEIGHT
            )
            pygame.draw.rect(self.screen, SimConfig.STATION_COLOR, station_rect)
            pygame.draw.rect(self.screen, SimConfig.REGION_BORDER, station_rect, 2)

            # Draw station label
            label = self.font.render(f"Station {i+1}", True, (0, 0, 0))
            self.screen.blit(label, (SimConfig.STATION_MARGIN + 10, station_y + 10))

            # Draw assigned boats (triangles)
            boat = next((b for b in boats if b.home_station == i), None)
            if boat and boat.state == "IDLE":
                self.draw_boat_triangle(
                    SimConfig.STATION_MARGIN + 40,
                    station_y + SimConfig.STATION_HEIGHT//2,
                    boat.id
                )

            # Draw assigned UAVs (circles)
            station_uavs = [u for u in uavs if u.home_station == i and u.state == "IDLE"]
            for j, uav in enumerate(station_uavs[:2]):  # Max 2 UAVs per station
                self.draw_uav_circle(
                    SimConfig.STATION_MARGIN + 120 + (j * 40),
                    station_y + SimConfig.STATION_HEIGHT//2,
                    uav.id
                )

    def draw_boat_triangle(self, x, y, boat_id):
        """Draw a boat as a triangle"""
        points = [
            (x, y - 10),  # Top
            (x - 10, y + 10),  # Bottom left
            (x + 10, y + 10)   # Bottom right
        ]
        pygame.draw.polygon(self.screen, SimConfig.BOAT_COLOR, points)
        label = self.small_font.render(boat_id, True, (0, 0, 0))
        self.screen.blit(label, (x - 15, y + 15))

    def draw_uav_circle(self, x, y, uav_id):
        """Draw a UAV as a circle"""
        pygame.draw.circle(self.screen, SimConfig.UAV_COLOR, (x, y), 10)
        label = self.small_font.render(uav_id, True, (0, 0, 0))
        self.screen.blit(label, (x - 15, y + 15))

    def draw_rescue_area(self, uavs, boats, victims):
        """Draw the rescue operation area"""
        rescue_x = SimConfig.STATION_REGION_WIDTH

        # Draw active agents in the rescue area
        for uav in uavs:
            if uav.state != "IDLE":
                x = rescue_x + int(uav.position.x)
                y = int(uav.position.y)
                pygame.draw.circle(self.screen, SimConfig.UAV_COLOR, (x, y), 10)

        for boat in boats:
            if boat.state != "IDLE":
                x = rescue_x + int(boat.position.x)
                y = int(boat.position.y)
                self.draw_boat_triangle(x, y, boat.id)

        # Draw victims
        for victim in victims:
            x = rescue_x + int(victim.position.x)
            y = int(victim.position.y)
            pygame.draw.circle(self.screen, SimConfig.VICTIM_COLOR, (x, y), 5)

    def draw_legend(self):
        """Draw legend in the right region"""
        legend_x = SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_WIDTH + 10
        legend_y = 20

        # Draw legend title
        title = self.font.render("LEGEND", True, (0, 0, 0))
        self.screen.blit(title, (legend_x, legend_y))

        # Legend items with their symbols and descriptions
        legend_items = [
            ("Station", SimConfig.STATION_COLOR, "rectangle"),
            ("UAV", SimConfig.UAV_COLOR, "circle"),
            ("Rescue Boat", SimConfig.BOAT_COLOR, "triangle"),
            ("Victim", SimConfig.VICTIM_COLOR, "circle"),
            ("Discovered Victim", (255, 165, 0), "circle"),  # Orange
            ("Victim Being Rescued", (255, 255, 0), "circle")  # Yellow
        ]

        # Draw each legend item
        for i, (label, color, shape) in enumerate(legend_items):
            y_pos = legend_y + 40 + (i * 30)

            # Draw symbol based on shape type
            if shape == "circle":
                pygame.draw.circle(
                    self.screen,
                    color,
                    (legend_x + 15, y_pos + 7),
                    7
                )
            elif shape == "triangle":
                points = [
                    (legend_x + 15, y_pos),  # Top
                    (legend_x + 5, y_pos + 15),  # Bottom left
                    (legend_x + 25, y_pos + 15)  # Bottom right
                ]
                pygame.draw.polygon(self.screen, color, points)
            elif shape == "rectangle":
                pygame.draw.rect(
                    self.screen,
                    color,
                    (legend_x + 5, y_pos, 20, 15)
                )

            # Draw label
            label_surface = self.small_font.render(label, True, (0, 0, 0))
            self.screen.blit(label_surface, (legend_x + 35, y_pos))

        # Draw state information
        state_y = legend_y + 250
        title = self.font.render("AGENT STATES", True, (0, 0, 0))
        self.screen.blit(title, (legend_x, state_y))

        states = [
            ("IDLE", (128, 128, 128)),      # Gray
            ("SCOUTING", (0, 255, 0)),      # Green
            ("RESCUING", (255, 165, 0)),    # Orange
            ("RETURNING", (0, 0, 255)),     # Blue
            ("MONITORING", (255, 255, 0))   # Yellow
        ]

        for i, (state, color) in enumerate(states):
            y_pos = state_y + 40 + (i * 30)
            pygame.draw.rect(
                self.screen,
                color,
                (legend_x + 5, y_pos, 20, 15)
            )
            state_label = self.small_font.render(state, True, (0, 0, 0))
            self.screen.blit(state_label, (legend_x + 35, y_pos))

        # Draw statistics
        stats_y = state_y + 250
        title = self.font.render("STATISTICS", True, (0, 0, 0))
        self.screen.blit(title, (legend_x, stats_y))

        stats = [
            f"Active UAVs: {len([u for u in self.active_uavs])}",
            f"Active Boats: {len([b for b in self.active_boats])}",
            f"Victims Found: {self.victims_found}",
            f"Victims Rescued: {self.victims_rescued}",
            f"Total Victims: {self.total_victims}"
        ]

        for i, stat in enumerate(stats):
            y_pos = stats_y + 40 + (i * 25)
            stat_label = self.small_font.render(stat, True, (0, 0, 0))
            self.screen.blit(stat_label, (legend_x + 5, y_pos))

    def update_stats(self, uavs, boats, victims):
        """Update statistics for the legend"""
        self.active_uavs = [u for u in uavs if u.state != "IDLE"]
        self.active_boats = [b for b in boats if b.state != "IDLE"]
        self.victims_found = len([v for v in victims if hasattr(v, 'discovered') and v.discovered])
        self.victims_rescued = len([v for v in victims if not v.active])
        self.total_victims = len(victims)

    def start_detection_flash(self, uav_id):
        self.detection_flashes[uav_id] = self.detection_flash_duration