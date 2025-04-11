from flask import Flask, request, jsonify, render_template
import logging
import models

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Инициализация устройств
logger.info("Initializing devices...")
sensor = models.Sensor("Temperature Sensor")
robot = models.Robot("Main Robot")
lamp = models.SignalLamp("Status Lamp", "red")
mech_robot = models.MechanicalRobot("Mechanical Robot")
vac_robot = models.VacuumRobot("Vacuum Robot")
logger.info("Devices initialized successfully")


def get_device(device_type):
    return {
        'sensor': sensor,
        'robot': robot,
        'lamp': lamp,
        'mechanical_robot': mech_robot,
        'vacuum_robot': vac_robot
    }.get(device_type)


@app.route('/connect', methods=['POST'])
def connect():
    try:
        command_data = request.get_json()
        logger.info(f"Received /connect request: {command_data}")

        device_type = command_data.get('device_type')
        device = get_device(device_type)

        if not device:
            logger.error(f"Unknown device type: {device_type}")
            return jsonify({"error": "Unknown device type"}), 400

        response = device.connect(command_data)
        logger.info(f"Response: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in /connect: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/control_all', methods=['POST'])
def control_all():
    try:
        commands = request.get_json()
        logger.info(f"Received /control_all request: {commands}")
        responses = {}

        for device_key, command_data in commands.items():
            device = get_device(device_key)
            if device:
                responses[device_key] = device.connect(command_data)
            else:
                responses[device_key] = {"error": "Unknown device type"}

        return jsonify({"status": "success", "responses": responses})

    except Exception as e:
        logger.error(f"Error in /control_all: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    logger.info("Serving index page")
    return render_template('index.html')


if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
