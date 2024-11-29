from .base import Entity, AgentState
from simulation.config import SimConfig
import math

class Boat(Entity):
    def __init__(self, id: str, x: float, y: float, home_station: int = 0):
        super().__init__(id, x, y)
        self.velocity = 0.375
        self.rescue_capacity = 5
        self.rescued_count = 0
        self.detection_radius = 30
        self.home_station = home_station
        self.state = "IDLE"
        self.target = None
        self.has_victim = False

    def update(self):
        """Update boat position and state"""
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
        """Detect victims within boat's smaller radius"""
        detected = []
        for victim in victims:
            if (victim.active and
                self.position.distance_to(victim.position) <= self.detection_radius):
                detected.append(victim)
        return detected