import pygame
import random
import math
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict
from enum import Enum
import logging
import time
from communication import Message
import pygame.gfxdraw

# Constants
WINDOW_SIZE = (800, 600)
STATION_POS = (50, 50)
UAV_SPEED = 5
BOAT_SPEED = 3
DETECTION_RADIUS = 50

# Colors
UAV_COLOR = (0, 255, 0)
BOAT_COLOR = (0, 0, 255)
VICTIM_COLOR = (255, 0, 0)
STATION_COLOR = (255, 255, 0)

class AgentState(Enum):
    IDLE = "idle"
    SCOUTING = "scouting"
    RESCUING = "rescuing"
    RETURNING = "returning"
    MONITORING = "monitoring"

@dataclass
class Position:
    x: float
    y: float

    def distance_to(self, other: 'Position') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Entity:
    def __init__(self, id: str, x: float, y: float):
        self.id = id
        self.position = Position(x, y)
        self.active = True
        self.state = AgentState.IDLE
        self.target = None
        self.path = []
        self.battery = 100

    def move_towards(self, target_x: float, target_y: float, speed: float):
        dx = target_x - self.position.x
        dy = target_y - self.position.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.position.x += (dx/distance) * speed
            self.position.y += (dy/distance) * speed
            self.battery -= 0.1  # Battery consumption

    def update_path(self, target_pos: Position):
        # Simple A* pathfinding could be implemented here
        self.path = [(target_pos.x, target_pos.y)]

class UAV(Entity):
    def __init__(self, id: str, x: float, y: float):
        super().__init__(id, x, y)
        self.has_buoy = True
        self.torch_battery = 100
        self.scan_pattern = self.generate_scan_pattern()
        self.current_pattern_index = 0

    def generate_scan_pattern(self):
        # Generate lawnmower pattern
        pattern = []
        x_steps = np.arange(100, WINDOW_SIZE[0]-100, 100)
        y_steps = np.arange(100, WINDOW_SIZE[1]-100, 100)

        for i, x in enumerate(x_steps):
            if i % 2 == 0:
                for y in y_steps:
                    pattern.append((x, y))
            else:
                for y in reversed(y_steps):
                    pattern.append((x, y))
        return pattern

    def detect_victims(self, victims: List['Victim']) -> List['Victim']:
        detected = []
        for victim in victims:
            if victim.active and self.position.distance_to(victim.position) <= DETECTION_RADIUS:
                detected.append(victim)
        return detected

    def update_scout_pattern(self):
        if self.state == AgentState.SCOUTING:
            if self.current_pattern_index < len(self.scan_pattern):
                next_point = self.scan_pattern[self.current_pattern_index]
                if self.position.distance_to(Position(*next_point)) < 5:
                    self.current_pattern_index += 1

class Boat(Entity):
    def __init__(self, id: str, x: float, y: float):
        super().__init__(id, x, y)
        self.rescue_capacity = 5
        self.rescued_count = 0

class Victim(Entity):
    def __init__(self, id: str, x: float, y: float):
        super().__init__(id, x, y)
        self.distress_level = random.randint(1, 5)
        self.discovered = False
        self.being_monitored = False
        self.discovery_time = None
        self.monitor_start_time = None
        self.rescue_start_time = None

    def discover(self):
        """Mark victim as discovered"""
        if not self.discovered:
            self.discovered = True
            self.discovery_time = time.time()

    def start_monitoring(self):
        """Start monitoring the victim"""
        self.being_monitored = True
        self.monitor_start_time = time.time()

    def stop_monitoring(self):
        """Stop monitoring the victim"""
        self.being_monitored = False

    def start_rescue(self):
        """Start rescue operation"""
        self.rescue_start_time = time.time()

    def get_wait_time(self) -> float:
        """Get time since discovery"""
        if self.discovery_time:
            return time.time() - self.discovery_time
        return 0

class RescueSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Sea Rescue Simulation")
        self.clock = pygame.time.Clock()
        self.stats = {
            'victims_rescued': 0,
            'victims_discovered': 0,
            'total_distance': 0
        }

        # Initialize entities
        self.uavs = [UAV(f"uav_{i}", STATION_POS[0], STATION_POS[1])
                    for i in range(3)]
        self.boats = [Boat(f"boat_{i}", STATION_POS[0], STATION_POS[1])
                     for i in range(2)]
        self.victims = self.generate_random_victims(5)
        self.running = True
        self.messages = []
        self.font = pygame.font.Font(None, 20)

    def execute_command(self, agent_id: str, command: str, params: Dict):
        agent = self.find_agent(agent_id)
        if not agent:
            return {'status': 'error', 'message': 'Agent not found'}

        if command == 'scout':
            agent.state = AgentState.SCOUTING
            return {'status': 'success'}

        elif command == 'goto':
            x, y = params['x'], params['y']
            agent.target = Position(x, y)
            agent.update_path(agent.target)
            return {'status': 'success'}

        elif command == 'return_to_station':
            agent.target = Position(*STATION_POS)
            agent.state = AgentState.RETURNING
            return {'status': 'success'}

        return {'status': 'error', 'message': 'Unknown command'}

    def find_agent(self, agent_id: str):
        for agent in self.uavs + self.boats:
            if agent.id == agent_id:
                return agent
        return None

    def update(self):
        # Update UAVs
        for uav in self.uavs:
            if uav.state == AgentState.SCOUTING:
                uav.update_scout_pattern()
                detected = uav.detect_victims(self.victims)
                for victim in detected:
                    if not victim.discovered:
                        victim.discovered = True
                        self.stats['victims_discovered'] += 1
                        logging.info(f"Victim discovered by {uav.id}")

            if uav.target:
                prev_pos = (uav.position.x, uav.position.y)
                uav.move_towards(uav.target.x, uav.target.y, UAV_SPEED)
                self.stats['total_distance'] += math.dist(
                    prev_pos, (uav.position.x, uav.position.y))

        # Update boats
        for boat in self.boats:
            if boat.target and boat.state == AgentState.RESCUING:
                prev_pos = (boat.position.x, boat.position.y)
                boat.move_towards(boat.target.x, boat.target.y, BOAT_SPEED)
                self.stats['total_distance'] += math.dist(
                    prev_pos, (boat.position.x, boat.position.y))

                # Check for rescue completion
                if isinstance(boat.target, Victim) and \
                   boat.position.distance_to(boat.target.position) < 5:
                    boat.target.active = False
                    boat.target = None
                    boat.state = AgentState.RETURNING
                    self.stats['victims_rescued'] += 1

    def draw(self):
        self.screen.fill((200, 200, 255))

        # Draw station
        pygame.draw.circle(self.screen, STATION_COLOR, STATION_POS, 10)

        # Draw paths
        for entity in self.uavs + self.boats:
            if entity.path:
                points = [(entity.position.x, entity.position.y)] + entity.path
                pygame.draw.lines(self.screen, (100, 100, 100), False, points, 1)

        # Draw entities
        for victim in self.victims:
            if victim.active:
                color = VICTIM_COLOR if not victim.discovered else (255, 165, 0)
                pygame.draw.circle(self.screen, color,
                                 (int(victim.position.x), int(victim.position.y)), 5)

        for uav in self.uavs:
            pygame.draw.circle(self.screen, UAV_COLOR,
                             (int(uav.position.x), int(uav.position.y)), 7)
            # Draw detection radius
            pygame.draw.circle(self.screen, (0, 255, 0, 50),
                             (int(uav.position.x), int(uav.position.y)),
                             DETECTION_RADIUS, 1)

        for boat in self.boats:
            pygame.draw.circle(self.screen, BOAT_COLOR,
                             (int(boat.position.x), int(boat.position.y)), 8)

        # Draw stats
        self.draw_stats()

        self.draw_communication_lines()

        pygame.display.flip()

    def draw_stats(self):
        font = pygame.font.Font(None, 24)
        stats_text = [
            f"Victims Rescued: {self.stats['victims_rescued']}",
            f"Victims Discovered: {self.stats['victims_discovered']}",
            f"Total Distance: {int(self.stats['total_distance'])}m"
        ]

        for i, text in enumerate(stats_text):
            surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(surface, (10, WINDOW_SIZE[1] - 30 * (len(stats_text) - i)))

    def add_message(self, sender: str, receiver: str, content: str):
        message = Message(
            sender=sender,
            receiver=receiver,
            content=content,
            timestamp=time.time()
        )
        self.messages.append(message)

    def draw_communication_lines(self):
        # Remove expired messages
        self.messages = [m for m in self.messages if not m.is_expired()]

        for message in self.messages:
            # Find sender and receiver positions
            sender_pos = self.get_agent_position(message.sender)
            receiver_pos = self.get_agent_position(message.receiver)

            if sender_pos and receiver_pos:
                # Calculate message progress (0 to 1)
                progress = (time.time() - message.timestamp) / message.duration

                # Interpolate message position
                current_x = sender_pos[0] + (receiver_pos[0] - sender_pos[0]) * progress
                current_y = sender_pos[1] + (receiver_pos[1] - sender_pos[1]) * progress

                # Draw communication line
                pygame.draw.line(self.screen, (255, 255, 255),
                               sender_pos, receiver_pos, 1)

                # Draw moving message dot
                pygame.draw.circle(self.screen, (255, 255, 0),
                                 (int(current_x), int(current_y)), 3)

                # Draw message content
                text_surface = self.font.render(message.content, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(current_x, current_y - 10))
                self.screen.blit(text_surface, text_rect)

    def get_agent_position(self, agent_id: str) -> Tuple[int, int]:
        # Find agent by ID and return its position
        for agent in self.uavs + self.boats:
            if agent.id == agent_id:
                return (int(agent.position.x), int(agent.position.y))
        return None

    def run(self):
        from api_server import start_api
        start_api(self)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 1:  # Left click
                        self.add_victim(x, y)
                    elif event.button == 3:  # Right click
                        # Remove nearest victim for testing
                        victim, dist = self.get_nearest_victim(Position(x, y))
                        if victim and dist < 20:  # Within 20 pixels
                            self.remove_victim(victim)

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def generate_random_victims(self, count: int) -> List[Victim]:
        """Generate random victims on the map, avoiding the station area"""
        victims = []
        min_distance_between = 50  # Minimum distance between victims
        station_safe_radius = 100  # Keep victims away from station

        for i in range(count):
            while True:
                # Generate random position
                x = random.randint(100, WINDOW_SIZE[0]-100)
                y = random.randint(100, WINDOW_SIZE[1]-100)

                # Check distance from station
                if math.dist((x, y), STATION_POS) < station_safe_radius:
                    continue

                # Check distance from other victims
                too_close = False
                for v in victims:
                    if math.dist((x, y), (v.position.x, v.position.y)) < min_distance_between:
                        too_close = True
                        break

                if not too_close:
                    victim = Victim(f"victim_{i}", x, y)
                    victims.append(victim)
                    break

        return victims

    def add_victim(self, x: float, y: float):
        """Add a new victim at specified position"""
        victim_id = f"victim_{len(self.victims)}"
        victim = Victim(victim_id, x, y)
        self.victims.append(victim)
        logging.info(f"New victim {victim_id} added at ({x}, {y})")
        return victim

    def remove_victim(self, victim: Victim):
        """Remove a victim (after rescue)"""
        if victim in self.victims:
            self.victims.remove(victim)
            self.stats['victims_rescued'] += 1
            logging.info(f"Victim {victim.id} rescued and removed")

    def get_active_victims(self) -> List[Victim]:
        """Get list of active (not rescued) victims"""
        return [v for v in self.victims if v.active]

    def get_discovered_victims(self) -> List[Victim]:
        """Get list of discovered but not rescued victims"""
        return [v for v in self.victims if v.discovered and v.active]

    def get_nearest_victim(self, pos: Position) -> Tuple[Victim, float]:
        """Find nearest active victim to given position"""
        active_victims = self.get_active_victims()
        if not active_victims:
            return None, float('inf')

        distances = [(v, pos.distance_to(v.position)) for v in active_victims]
        return min(distances, key=lambda x: x[1])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sim = RescueSimulation()
    sim.run()