from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class SimConfig:
    # Window and Region Sizes
    WINDOW_SIZE = (1400, 800)

    # Region dimensions
    STATION_REGION_WIDTH = 250
    LEGEND_REGION_WIDTH = 250
    RESCUE_REGION_WIDTH = WINDOW_SIZE[0] - (STATION_REGION_WIDTH + LEGEND_REGION_WIDTH)

    # Station dimensions
    STATION_HEIGHT = 120  # Reduced height
    STATION_WIDTH = 220
    STATION_MARGIN = 15   # Reduced margin
    STATION_TOP_MARGIN = 30  # Margin from top of screen

    # Rescue region boundaries (for victim spawning)
    RESCUE_REGION_MARGIN = 50  # Margin from edges

    # Colors
    STATION_COLOR = (200, 200, 200)
    UAV_COLOR = (0, 255, 0)
    BOAT_COLOR = (0, 0, 255)
    VICTIM_COLOR = (255, 0, 0)
    REGION_BORDER = (100, 100, 100)

    # Simulation parameters
    TICK_RATE = 60

    # Agent counts
    NUM_UAVS = 10
    NUM_BOATS = 5
    NUM_VICTIMS = 10
    NUM_STATIONS = 5

    # Station positions
    STATION_POSITIONS = [
        (100, 100),   # Station 1 (NW)
        (1100, 100),  # Station 2 (NE)
        (600, 400),   # Station 3 (Center)
        (100, 700),   # Station 4 (SW)
        (1100, 700)   # Station 5 (SE)
    ]

    # Agent speeds and capabilities
    UAV_SPEED = 5
    BOAT_SPEED = 3
    DETECTION_RADIUS = 50