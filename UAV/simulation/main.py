from simulation.core.simulation import RescueSimulation
from simulation.api.server import start_api_server
import argparse

def main():
    parser = argparse.ArgumentParser(description='UAV Rescue Simulation')
    parser.add_argument('--api-port', type=int, default=5000,
                       help='Port for the API server')
    args = parser.parse_args()

    # Start simulation
    sim = RescueSimulation()

    # Start API server
    start_api_server(sim, port=args.api_port)

    # Run simulation
    sim.run()

if __name__ == "__main__":
    main()