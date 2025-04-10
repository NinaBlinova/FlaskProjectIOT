from flask import Flask, request, render_template, jsonify
import logging
from abc import ABC, abstractmethod

from flask import Flask, jsonify, render_template
import models

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)

# Создаем экземпляры устройств
logger.info("Creating devices...")
sensor = models.Sensor("Temperature Sensor")
robot = models.Robot("Main Robot")
lamp = models.SignalLamp("Status Lamp", "red")
mech_robot = models.MechanicalRobot("Mechanical Robot")
vac_robot = models.VacuumRobot("Vacuum Robot")
models.logger.info("All devices created")


@app.route('/connect', methods=['POST'])
def connect():
    try:
        command_data = request.json
        logger.info(f"Received connect request: {command_data}")
        device_type = command_data.get('device_type')

        if device_type == 'sensor':
            response = sensor.connect(command_data)
        elif device_type == 'robot':
            response = robot.connect(command_data)
        elif device_type == 'lamp':
            response = lamp.connect(command_data)
        elif device_type == 'mechanical_robot':
            response = mech_robot.connect(command_data)
        elif device_type == 'vacuum_robot':
            response = vac_robot.connect(command_data)
        else:
            logger.error(f"Unknown device type: {device_type}")
            return jsonify({"error": "Unknown device type"}), 400

        logger.info(f"Returning response: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in connect: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/control_all', methods=['POST'])
def control_all():
    try:
        commands = request.json
        logger.info(f"Received control_all request: {commands}")
        responses = {}

        if 'sensor' in commands:
            responses['sensor'] = sensor.connect(commands['sensor'])
        if 'robot' in commands:
            responses['robot'] = robot.connect(commands['robot'])
        if 'lamp' in commands:
            responses['lamp'] = lamp.connect(commands['lamp'])
        if 'mechanical_robot' in commands:
            responses['mechanical_robot'] = mech_robot.connect(commands['mechanical_robot'])
        if 'vacuum_robot' in commands:
            responses['vacuum_robot'] = vac_robot.connect(commands['vacuum_robot'])

        logger.info(f"Returning control_all responses: {responses}")
        return jsonify({"status": "success", "responses": responses})
    except Exception as e:
        logger.error(f"Error in control_all: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    logger.info("Serving index page")
    return render_template('index.html')


if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
