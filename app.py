import logging
import time
import threading

from flask import Flask, jsonify, render_template
import models

app = Flask(__name__)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ====================== Функции для получения данных (AJAX endpoints) ======================

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


@app.route('/get_sensor_data')
def get_sensor_data():
    return jsonify(sensor.emulate_data())

@app.route('/get_lamp_data')
def get_lamp_data():
    return jsonify(lamp.emulate_data())

@app.route('/get_robot_data')
def get_robot_data():
    return jsonify(robot.emulate_data())

@app.route('/get_mech_robot_data')
def get_mech_robot_data():
    return jsonify(rob_meh.emulate_data())

@app.route('/get_vacuum_robot_data')
def get_vacuum_robot_data():
    return jsonify(vac_rob.emulate_data())
# ====================== Главная страница (отображение данных) ======================
@app.route("/")
def main():
    return render_template('index.html',
                           sensor_name=sensor.name,
                           lamp_name=lamp.name,
                           robot_name=robot.name,
                           mech_robot_name=rob_meh.name,
                           vacuum_robot_name=vac_rob.name)

# ====================== Фоновое обновление данных ======================
def update_data():
    while True:
        # Вызываем emulate_data() для каждого объекта, чтобы обновить их состояние
        sensor.emulate_data()
        lamp.emulate_data()
        robot.emulate_data()
        rob_meh.emulate_data()
        vac_rob.emulate_data()
        time.sleep(5)  # Обновляем данные каждые 5 секунд

# Запускаем фоновый поток для обновления данных
data_thread = threading.Thread(target=update_data)
data_thread.daemon = True  # Завершаем поток при завершении приложения
data_thread.start()

# ====================== Запуск приложения ======================
if __name__ == '__main__':
    app.run(debug=True)
