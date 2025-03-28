import logging
import random
from abc import ABC, abstractmethod

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Thing(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def include_in_system(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    def is_in_system(self):
        """Проверяет, включена ли вещь в систему."""
        return self.in_system


class Robot(Thing):
    def __init__(self, name):
        super().__init__(name)
        # Параметры для мониторинга (от оборудования)
        self.lastCommand = 0
        self.status = 0
        self.count = 0
        # Параметры для управления (на оборудование)
        self.coordX = 0
        self.coordY = 0
        self.temperature = 0
        self.commandNumber = 0
        logger.info(f"Robot initialized: {self.name}")

    def include_in_system(self):
        logger.info(f"Robot included in system: {self.name}")

    def get_status(self):
        logger.info(f"Robot status: {self.status}")
        return self.status

    def get_coordinates(self):
        logger.info(f"Robot coordinates: {self.coordX}, {self.coordY}")
        return self.coordX, self.coordY

    def get_temperature(self):
        logger.info(f"Robot temperature: {self.temperature}")
        return self.temperature

    def get_last_command(self):
        logger.info(f"Robot last command: {self.lastCommand}")
        return self.lastCommand

    def get_count(self):
        logger.info(f"Robot count command: {self.count}")
        return self.count

    def set_status(self, status):
        self.status = status
        logger.info(f"Robot status set to: {self.status}")

    def set_temperature(self, temperature):
        self.temperature = temperature
        logger.info(f"Robot temperature set to: {self.temperature}")

    def set_commandNumber(self, commandNumber):
        self.commandNumber = commandNumber
        logger.info(f"Robot commandNumber set to: {self.commandNumber}")

    def set_coordX(self, coordX):
        self.coordX = coordX
        logger.info(f"Robot coordX set to: {self.coordX}")

    def set_coordY(self, coordY):
        self.coordY = coordY
        logger.info(f"Robot coordY set to: {self.coordY}")

    def startCommand(self):
        logger.info(f"Robot start command: {self.commandNumber}")

    def emulate_data(self):
        """Эмулирует данные для робота (мониторинг)."""
        self.status = random.choice([0, 1])  # 0 - idle, 1 - working
        self.coordX = random.randint(0, 100)
        self.coordY = random.randint(0, 100)
        self.temperature = random.uniform(20, 30)
        self.commandNumber = random.randint(1, 10)

        data = {
            'status': self.status,
            'coordX': self.coordX,
            'coordY': self.coordY,
            'temperature': self.temperature,
            'commandNumber': self.commandNumber,
            'name': self.name
        }
        return data


class MechanicalRobor(Robot):
    def __init__(self, name):
        super().__init__(name)
        self.angle = 0
        self.grab = 0

    def set_angle(self, angle):
        self.angle = angle
        logger.info(f"Robot angle set to: {self.angle}")

    def set_grab(self, grab):
        self.grab = grab
        logger.info(f"Robot grab set to: {self.grab}")

    def emulate_data(self):
        """Эмулирует данные для механического робота (мониторинг)."""
        self.angle = random.randint(0, 360)
        self.grab = random.choice([0, 1])  # 0 - not grabbing, 1 - grabbing

        data = {
            'status': self.status, # Inherited
            'coordX': self.coordX, # Inherited
            'coordY': self.coordY, # Inherited
            'temperature': self.temperature, # Inherited
            'commandNumber': self.commandNumber, # Inherited
            'angle': self.angle,
            'grab': self.grab,
            'name': self.name
        }
        return data


class VacuumRobor(Robot):
    def __init__(self, name):
        super().__init__(name)
        self.vacuum_capture = 0

    def set_vacuum_capture(self, vacuum_capture):
        self.vacuum_capture = vacuum_capture
        logger.info(f"Robot grab set to: {self.vacuum_capture}")

    def emulate_data(self):
        """Эмулирует данные для вакуумного робота (мониторинг)."""
        self.vacuum_capture = random.choice([0, 1])  # 0 - off, 1 - on
        self.temperature = random.uniform(25,35)
        data = {
            'status': self.status,
            'coordX': self.coordX,
            'coordY': self.coordY,
            'temperature': self.temperature, # Inherited
            'commandNumber': self.commandNumber, # Inherited
            'vacuum_capture': self.vacuum_capture,
            'name': self.name
        }
        return data


class Sensor(Thing):
    def __init__(self, name, value=0):
        super().__init__(name)
        self.value = value
        logger.info(f"Sensor initialized: {self.name}, value: {value}")

    def get_status(self):
        status = f"Sensor {self.name}: {self.value}"
        logger.info(status)
        return status

    def include_in_system(self):
        logger.info(f"Sensor included in system: {self.name}")

    def update_value(self, new_value):
        self.value = new_value
        logger.info(f"Sensor {self.name} updated to {self.value}")

    def emulate_data(self):
        """Эмулирует данные для сенсора."""
        self.value = random.uniform(15, 35) # Emulate temp
        data = {
            'value': self.value,
            'name': self.name
        }
        return data


class SignalLamp(Thing):
    def __init__(self, name, color="red"):
        super().__init__(name)
        self.color = color
        logger.info(f"SignalLamp initialized: {self.name}, color: {color}")

    def get_status(self):
        status = f"SignalLamp {self.name} is {self.color}"
        logger.info(status)
        return status

    def include_in_system(self):
        logger.info(f"SignalLamp included in system: {self.name}")

    def change_color(self, new_color):
        self.color = new_color
        logger.info(f"SignalLamp {self.name} changed to {self.color}")

    def emulate_data(self):
        """Эмулирует данные для сигнальной лампы."""
        colors = ["red", "green", "yellow"]
        self.color = random.choice(colors) # Emulate changing color
        data = {
            'color': self.color,
            'name': self.name
        }
        return data
