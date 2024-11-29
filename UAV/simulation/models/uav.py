from .base import Entity, AgentState
from .position import Position
from ..config import SimConfig
import numpy as np
import math

class UAV(Entity):
    def __init__(self, id: str, x: float, y: float, home_station: int = 0):
        super().__init__(id, x, y)
        self.velocity = 0.375  # 15x faster than victim
        self.has_buoy = True
        self.detection_radius = 50
        self.home_station = home_station
        self.state = "IDLE"
        self.uav_id = int(id.replace("uav", ""))
        self.scan_pattern = None  # Initialize later
        self.current_pattern_index = 0
        self.following_victim = None
        self.rescue_boat = None

        # Ensure starting at correct base position
        self.position.x = x
        self.position.y = y
        self.target = None

    def generate_scan_pattern(self):
        """Generate lawnmower pattern for assigned region"""
        pattern = []
        # Calculate rescue region boundaries
        rescue_x_start = SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_MARGIN
        rescue_x_end = (SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_WIDTH
                       - SimConfig.LEGEND_REGION_WIDTH - SimConfig.RESCUE_REGION_MARGIN)
        rescue_y_start = SimConfig.RESCUE_REGION_MARGIN
        rescue_y_end = SimConfig.WINDOW_SIZE[1] - SimConfig.RESCUE_REGION_MARGIN

        # Split region into 10 vertical sections for 10 UAVs
        section_width = (rescue_x_end - rescue_x_start) / 10
        my_x_start = rescue_x_start + (self.uav_id - 1) * section_width
        my_x_end = my_x_start + section_width

        # Generate grid points with spacing based on detection radius
        x_steps = np.arange(my_x_start, my_x_end, self.detection_radius * 1.5)
        y_steps = np.arange(rescue_y_start, rescue_y_end, self.detection_radius * 1.5)

        # Create lawnmower pattern for assigned section
        for i, x in enumerate(x_steps):
            if i % 2 == 0:
                for y in y_steps:
                    pattern.append(Position(x, y))
            else:
                for y in reversed(y_steps):
                    pattern.append(Position(x, y))
        return pattern

    def update_scout_pattern(self):
        """Update position in scouting pattern"""
        if self.state == "SCOUTING":
            if self.current_pattern_index < len(self.scan_pattern):
                next_point = self.scan_pattern[self.current_pattern_index]
                if self.position.distance_to(next_point) < 5:
                    self.current_pattern_index += 1
                    if self.current_pattern_index >= len(self.scan_pattern):
                        self.current_pattern_index = 0  # Reset to continue scouting
                self.target = next_point

    def update(self):
        """Update UAV position and state"""
        if self.state == "MONITORING" and self.following_victim:
            # Follow victim
            self.target = self.following_victim.position
        elif self.state == "SCOUTING":
            self.update_scout_pattern()

        if self.target:
            # Calculate distance to target
            dx = self.target.x - self.position.x
            dy = self.target.y - self.position.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 5:  # Only move if not very close to target
                # Calculate velocity vector
                vx = (dx/distance) * self.velocity
                vy = (dy/distance) * self.velocity

                # Update position using velocity
                self.position.x += vx
                self.position.y += vy

    def detect_victims(self, victims):
        """Detect victims within radius"""
        detected = []
        for victim in victims:
            if (victim.active and not victim.discovered and
                self.position.distance_to(victim.position) <= self.detection_radius):
                detected.append(victim)
                # Start following first detected victim if not already following one
                if not self.following_victim:
                    self.following_victim = victim
                    self.state = "MONITORING"
        return detected

    def start_monitoring(self, victim):
        """Start monitoring a specific victim"""
        self.following_victim = victim
        self.state = "MONITORING"

    def stop_monitoring(self):
        """Stop monitoring current victim"""
        self.following_victim = None
        self.rescue_boat = None
        self.state = "SCOUTING"

    def start_scouting(self):
        """Initialize scouting pattern and start scouting"""
        if not self.scan_pattern:
            self.scan_pattern = self.generate_scan_pattern()
        self.state = "SCOUTING"
        self.current_pattern_index = 0
