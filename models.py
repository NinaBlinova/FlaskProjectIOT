import logging
import random
from abc import ABC, abstractmethod

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Thing(ABC):
    def __init__(self, name):
        self.name = name
        self.in_system = False
        logger.info(f"Thing {self.name} initialized")

    @abstractmethod
    def connect(self, command_data):
        pass


class Sensor(Thing):
    def __init__(self, name, unit="C"):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        self.power = "on"
        logger.info(f"Sensor {self.name} initialized with unit {self.unit}")

    def connect(self, command_data):
        if 'value' in command_data:
            old_value = self.value
            self.value = command_data['value']
            logger.info(f"Sensor {self.name} value changed from {old_value} to {self.value}")
        if 'power' in command_data:
            old_power = self.power
            self.power = command_data['power']
            logger.info(f"Sensor {self.name} power changed from {old_power} to {self.power}")
        return {
            "status": "success",
            "power": self.power,
            "value": self.value,
            "unit": self.unit
        }


class Robot(Thing):
    def __init__(self, name):
        super().__init__(name)
        self.status = 0
        self.coordinates = [0, 0]
        self.temperature = 25.0
        self.command_number = 0
        logger.info(f"Robot {self.name} initialized with coordinates {self.coordinates}")

    def connect(self, command_data):
        if 'status' in command_data:
            old_status = self.status
            self.status = command_data['status']
            logger.info(f"Robot {self.name} status changed from {old_status} to {self.status}")
        if 'coordinates' in command_data:
            old_coordinates = self.coordinates
            self.coordinates = command_data['coordinates']
            logger.info(f"Robot {self.name} coordinates changed from {old_coordinates} to {self.coordinates}")
        if 'temperature' in command_data:
            old_temp = self.temperature
            self.temperature = command_data['temperature']
            logger.info(f"Robot {self.name} temperature changed from {old_temp} to {self.temperature}")
        if 'command_number' in command_data:
            old_cmd = self.command_number
            self.command_number = command_data['command_number']
            logger.info(f"Robot {self.name} command number changed from {old_cmd} to {self.command_number}")

        return {
            "status": "success",
            "robot_status": self.status,
            "coordinates": self.coordinates,
            "temperature": self.temperature,
            "command_number": self.command_number
        }


class MechanicalRobot(Robot):
    def __init__(self, name):
        super().__init__(name)
        self.angle = 0
        self.grab = 0
        logger.info(f"MechanicalRobot {self.name} initialized with angle {self.angle} and grab {self.grab}")

    def connect(self, command_data):
        super().connect(command_data)

        if 'angle' in command_data:
            old_angle = self.angle
            self.angle = command_data['angle']
            logger.info(f"MechanicalRobot {self.name} angle changed from {old_angle} to {self.angle}")
        if 'grab' in command_data:
            old_grab = self.grab
            self.grab = command_data['grab']
            logger.info(f"MechanicalRobot {self.name} grab changed from {old_grab} to {self.grab}")

        return {
            "status": "success",
            "robot_status": self.status,
            "coordinates": self.coordinates,
            "angle": self.angle,
            "grab": self.grab
        }


class VacuumRobot(Robot):
    def __init__(self, name):
        super().__init__(name)
        self.vacuum_capture = 0
        logger.info(f"VacuumRobot {self.name} initialized with vacuum capture {self.vacuum_capture}")

        def connect(self, command_data):
            super().connect(command_data)

            if 'vacuum_capture' in command_data:
                old_capture = self.vacuum_capture
                self.vacuum_capture = command_data['vacuum_capture']
                logger.info(
                    f"VacuumRobot {self.name} vacuum capture changed from {old_capture} to {self.vacuum_capture}")

            return {
                "status": "success",
                "robot_status": self.status,
                "vacuum_capture": self.vacuum_capture,
                "temperature": self.temperature
            }


class SignalLamp(Thing):
    def __init__(self, name, color="red"):
        super().__init__(name)
        self.color = color
        self.power = "on"
        logger.info(f"SignalLamp {self.name} initialized with color {self.color}")

    def connect(self, command_data):
        if 'color' in command_data:
            old_color = self.color
            self.color = command_data['color']
            logger.info(f"SignalLamp {self.name} color changed from {old_color} to {self.color}")
        if 'power' in command_data:
            old_power = self.power
            self.power = command_data['power']
            logger.info(f"SignalLamp {self.name} power changed from {old_power} to {self.power}")

        return {
            "status": "success",
            "color": self.color,
            "power": self.power
        }
