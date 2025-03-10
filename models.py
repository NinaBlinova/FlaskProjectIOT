import logging
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


class Robot(Thing):
    def __init__(self, name):
        super().__init__(name)
        self.lastCommand = 0
        self.status = 0
        self.count = 0
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
