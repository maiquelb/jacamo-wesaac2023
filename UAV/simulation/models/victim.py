from .base import Entity
from ..config import SimConfig
import random
import time
import math

class Victim(Entity):
    def __init__(self, id: str, x: float, y: float):
        super().__init__(id, x, y)
        self.velocity = 0.025  # Reduced from 0.5 (20 times slower)
        self.distress_level = random.randint(1, 5)
        self.discovered = False
        self.direction_timer = 0
        self.current_direction = random.uniform(0, 2 * math.pi)
        self.discovery_time = None

    def discover(self):
        """Mark victim as discovered and record discovery time"""
        if not self.discovered:
            self.discovered = True
            self.discovery_time = time.time()

    def update(self):
        # Update direction periodically
        self.direction_timer += 1
        if self.direction_timer >= 60:  # Change direction every ~2 seconds
            self.direction_timer = 0
            self.current_direction = random.uniform(0, 2 * math.pi)

        # Move in current direction
        self.current_x_vel = math.cos(self.current_direction) * self.velocity
        self.current_y_vel = math.sin(self.current_direction) * self.velocity

        # Update position with boundary checking
        new_x = self.position.x + self.current_x_vel
        new_y = self.position.y + self.current_y_vel

        # Keep within rescue region bounds
        rescue_x_start = SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_MARGIN
        rescue_x_end = (SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_WIDTH
                       - SimConfig.LEGEND_REGION_WIDTH - SimConfig.RESCUE_REGION_MARGIN)
        rescue_y_start = SimConfig.RESCUE_REGION_MARGIN
        rescue_y_end = SimConfig.WINDOW_SIZE[1] - SimConfig.RESCUE_REGION_MARGIN

        if rescue_x_start <= new_x <= rescue_x_end:
            self.position.x = new_x
        else:
            self.current_direction = math.pi - self.current_direction

        if rescue_y_start <= new_y <= rescue_y_end:
            self.position.y = new_y
        else:
            self.current_direction = -self.current_direction