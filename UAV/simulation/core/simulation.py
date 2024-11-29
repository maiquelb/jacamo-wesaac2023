import pygame
import random
import math
from simulation.models.uav import UAV
from simulation.models.boat import Boat
from simulation.models.victim import Victim
from simulation.utils.visualization import Visualizer
from simulation.utils.logger import SimLogger
from simulation.core.communication import CommunicationSystem
from simulation.config import SimConfig
from typing import Dict
from simulation.models.position import Position

class RescueSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SimConfig.WINDOW_SIZE)
        pygame.display.set_caption("Sea Rescue Simulation")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize visualization
        self.visualizer = Visualizer(self.screen)
        self.communication = CommunicationSystem()

        # Initialize entities
        self.initialize_entities()

    def initialize_entities(self):
        # Initialize UAVs
        self.uavs = []
        for i in range(SimConfig.NUM_UAVS):
            station_idx = i % len(SimConfig.STATION_POSITIONS)
            x, y = SimConfig.STATION_POSITIONS[station_idx]
            uav = UAV(f"uav{i+1}", x, y, home_station=station_idx)
            uav.state = "IDLE"
            uav.position.x = x
            uav.position.y = y
            self.uavs.append(uav)

        # Initialize boats
        self.boats = []
        for i in range(SimConfig.NUM_BOATS):
            station_idx = i % len(SimConfig.STATION_POSITIONS)
            x, y = SimConfig.STATION_POSITIONS[station_idx]
            boat = Boat(f"boat{i+1}", x, y, home_station=station_idx)
            boat.state = "IDLE"
            boat.position.x = x
            boat.position.y = y
            self.boats.append(boat)

        # Generate victims
        self.victims = self.generate_random_victims(SimConfig.NUM_VICTIMS)

    def update(self):
        """Update simulation state"""
        # Update all victims
        for victim in self.victims:
            if victim.active:
                victim.update()

        # Update all agents
        for agent in self.uavs + self.boats:
            agent.update()

            # Check for victim detection
            if isinstance(agent, UAV) and agent.state == "SCOUTING":
                detected = agent.detect_victims(self.victims)
                if detected:
                    for victim in detected:
                        if not victim.discovered:
                            victim.discover()
                            self.visualizer.start_detection_flash(agent.id)
                            self.logger.info(f"{agent.id} detected victim: {victim.id}")

    def draw(self):
        """Draw the current simulation state"""
        self.visualizer.draw_all(
            self.uavs,
            self.boats,
            self.victims,
            self.communication
        )
        pygame.display.flip()

    def run(self):
        """Main simulation loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(SimConfig.TICK_RATE)

        pygame.quit()

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def execute_command(self, agent_id: str, command: str, params: Dict):
        """Execute commands from JaCaMo agents"""
        agent = self.find_agent(agent_id)
        if not agent:
            return {'status': 'error', 'message': 'Agent not found'}

        try:
            if command == 'scout':
                agent.state = "SCOUTING"
                if isinstance(agent, UAV):
                    agent.start_scouting()
                return {'status': 'success'}

            elif command == 'monitor':
                x, y = float(params['x']), float(params['y'])
                agent.state = "MONITORING"
                agent.target = Position(x, y)
                return {'status': 'success'}

            elif command == 'goto':
                x, y = float(params['x']), float(params['y'])
                agent.target = Position(x, y)
                if isinstance(agent, Boat):
                    agent.state = "RESCUING"
                return {'status': 'success'}

            elif command == 'return':
                station_pos = SimConfig.STATION_POSITIONS[agent.home_station]
                agent.target = Position(*station_pos)
                agent.state = "RETURNING"
                if isinstance(agent, UAV):
                    agent.stop_monitoring()
                return {'status': 'success'}

            return {'status': 'error', 'message': 'Unknown command'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def find_agent(self, agent_id: str):
        """Find an agent by ID"""
        for agent in self.uavs + self.boats:
            if agent.id == agent_id:
                return agent
        return None

    def generate_random_victims(self, count: int):
        """Generate random victims in the rescue region"""
        victims = []
        min_distance = 50  # Minimum distance between victims

        # Calculate rescue region boundaries
        rescue_x_start = SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_MARGIN
        rescue_x_end = (SimConfig.STATION_REGION_WIDTH + SimConfig.RESCUE_REGION_WIDTH
                       - SimConfig.LEGEND_REGION_WIDTH - SimConfig.RESCUE_REGION_MARGIN)
        rescue_y_start = SimConfig.RESCUE_REGION_MARGIN
        rescue_y_end = SimConfig.WINDOW_SIZE[1] - SimConfig.RESCUE_REGION_MARGIN

        for i in range(count):
            while True:
                x = random.randint(rescue_x_start, rescue_x_end)
                y = random.randint(rescue_y_start, rescue_y_end)
                pos = Position(x, y)

                # Check distance from other victims
                if all(pos.distance_to(v.position) > min_distance for v in victims):
                    victim = Victim(f"victim{i+1}", x, y)
                    victims.append(victim)
                    break

        return victims