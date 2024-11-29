from enum import Enum
from dataclasses import dataclass
from ..models.position import Position
import math

class AgentState(Enum):
    IDLE = "idle"
    SCOUTING = "scouting"
    RESCUING = "rescuing"
    RETURNING = "returning"
    MONITORING = "monitoring"

class Entity:
    def __init__(self, id: str, x: float, y: float):
        self.id = id
        self.position = Position(x, y)
        self.velocity = 2.0  # Base velocity for all entities
        self.active = True
        self.state = "IDLE"
        self.target = None
        self.path = []
        self.current_x_vel = 0
        self.current_y_vel = 0

    def move_towards(self, target_x: float, target_y: float):
        dx = target_x - self.position.x
        dy = target_y - self.position.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            # Normalize direction and apply velocity
            self.current_x_vel = (dx/distance) * self.velocity
            self.current_y_vel = (dy/distance) * self.velocity

            # Update position
            self.position.x += self.current_x_vel
            self.position.y += self.current_y_vel

    def update(self):
        if self.target:
            self.move_towards(self.target.x, self.target.y)