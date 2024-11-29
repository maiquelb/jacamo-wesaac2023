from flask import Flask, request, jsonify
from dataclasses import asdict
import threading
import json

app = Flask(__name__)

# Global reference to simulation instance
sim = None

@app.route('/agents', methods=['GET'])
def get_agents():
    agents = {
        'uavs': [asdict(uav) for uav in sim.uavs],
        'boats': [asdict(boat) for boat in sim.boats],
        'victims': [asdict(victim) for victim in sim.victims]
    }
    return jsonify(agents)

@app.route('/command', methods=['POST'])
def send_command():
    data = request.json
    agent_id = data['agent_id']
    command = data['command']
    params = data.get('params', {})

    result = sim.execute_command(agent_id, command, params)
    return jsonify(result)

@app.route('/communicate', methods=['POST'])
def send_message():
    data = request.json
    sender_id = data['sender']
    receiver_id = data['receiver']
    content = data['content']

    sim.add_message(sender_id, receiver_id, content)
    return jsonify({'status': 'success'})

def start_api(simulation, port=5000):
    global sim
    sim = simulation
    threading.Thread(target=lambda: app.run(port=port), daemon=True).start()