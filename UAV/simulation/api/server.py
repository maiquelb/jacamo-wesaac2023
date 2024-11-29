from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)
simulation = None

@app.route('/command', methods=['POST'])
def execute_command():
    data = request.json
    agent_id = data['agent_id']
    command = data['command']
    params = data.get('params', {})

    result = simulation.execute_command(agent_id, command, params)
    return jsonify(result)

@app.route('/agents', methods=['GET'])
def get_agents():
    agents_data = {
        'uavs': [{'id': uav.id,
                  'position': {'x': uav.position.x, 'y': uav.position.y},
                  'state': uav.state,
                  'detected_victims': len(uav.detect_victims(simulation.victims))}
                 for uav in simulation.uavs],
        'boats': [{'id': boat.id,
                  'position': {'x': boat.position.x, 'y': boat.position.y},
                  'state': boat.state}
                 for boat in simulation.boats]
    }
    return jsonify(agents_data)

def start_api_server(sim_instance, port=5000):
    global simulation
    simulation = sim_instance
    Thread(target=lambda: app.run(port=port), daemon=True).start()