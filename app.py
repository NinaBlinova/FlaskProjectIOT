import logging
from flask import Flask
import models

app = Flask(__name__)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route("/")
def main():
    logger.info("Initializing application and devices...")
    sensor = models.Sensor("Temperature", 25)
    lamp = models.SignalLamp("Warning Lamp", "green")
    robot = models.Robot("Example Robot")
    logger.info("Sensor initialized.")
    sensor.get_status()
    sensor.include_in_system()
    sensor.update_value(5)
    logger.info("Lamp initialized.")
    lamp.get_status()
    lamp.include_in_system()
    lamp.change_color("green")
    logger.info("Robot initialized.")
    robot.get_status()
    robot.include_in_system()
    robot.get_coordinates()
    rob_meh = models.MechanicalRobor("Example Mechanical Robot")
    logger.info("Mechanical robot initialized.")
    rob_meh.set_status(1)
    rob_meh.get_status()
    rob_meh.include_in_system()
    vac_rob = models.VacuumRobor("Example Vacuum Robor")
    logger.info("Vacuum robot initialized.")
    vac_rob.set_status(1)
    vac_rob.get_status()
    vac_rob.include_in_system()

    return "Devices initialized and logged."


if __name__ == '__main__':
    app.run(debug=True)
