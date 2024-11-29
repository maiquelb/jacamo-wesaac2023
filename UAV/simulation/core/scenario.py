import random
from simulation.models.position import Position
from simulation.config import ScenarioConfig
from simulation.models.victim import Victim
from simulation.models.uav import UAV
from simulation.models.boat import Boat

class ScenarioGenerator:
    def __init__(self, config: ScenarioConfig):
        self.config = config

    def generate_scenario(self):
        """Generate a complete rescue scenario"""
        stations = self.config.STATION_POSITIONS
        scenario = {
            'stations': stations,
            'uavs': self.generate_uavs(stations),
            'boats': self.generate_boats(stations),
            'victims': self.generate_victims()
        }
        return scenario

    def generate_victims(self) -> List[Victim]:
        """Generate victims in random positions"""
        victims = []
        min_distance = 50  # Minimum distance between victims

        for i in range(self.config.NUM_VICTIMS):
            while True:
                x = random.randint(100, self.config.MAP_WIDTH - 100)
                y = random.randint(100, self.config.MAP_HEIGHT - 100)

                # Check distance from other victims
                pos = Position(x, y)
                if all(pos.distance_to(v.position) > min_distance for v in victims):
                    victim = Victim(f"victim_{i}", x, y)
                    victim.distress_level = random.randint(1, 5)
                    victims.append(victim)
                    break

        return victims

    def generate_uavs(self, stations) -> List[UAV]:
        """Generate UAVs distributed across stations"""
        uavs = []
        for i in range(self.config.NUM_UAVS):
            station = random.choice(stations)
            uav = UAV(f"uav_{i}", station[0], station[1])
            uav.home_station = station
            uavs.append(uav)
        return uavs

    def generate_boats(self, stations) -> List[Boat]:
        """Generate boats distributed across stations"""
        boats = []
        for i in range(self.config.NUM_BOATS):
            station = random.choice(stations)
            boat = Boat(f"boat_{i}", station[0], station[1])
            boat.home_station = station
            boats.append(boat)
        return boats