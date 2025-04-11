import logging
import re
from abc import ABC, abstractmethod

# Настройка логирования
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

    def validate_float(self, value, field_name):
        """Проверка и преобразование к float"""
        try:
            return float(value)
        except (ValueError, TypeError):
            logger.error(f"Invalid float value for {field_name}: {value}")
            raise ValueError(f"Некорректное значение {field_name}: должно быть числом")

    def validate_int(self, value, field_name):
        """Проверка и преобразование к int"""
        try:
            return int(value)
        except (ValueError, TypeError):
            logger.error(f"Invalid int value for {field_name}: {value}")
            raise ValueError(f"Некорректное значение {field_name}: должно быть целым числом")

    def validate_string(self, value, field_name, pattern=None, options=None):
        """Проверка строки с опциональным regex или списком допустимых значений"""
        if not isinstance(value, str):
            raise ValueError(f"Некорректное значение {field_name}: должно быть строкой")

        if pattern and not pattern.match(value):
            raise ValueError(f"Некорректное значение {field_name}: не соответствует формату")

        if options and value not in options:
            raise ValueError(f"Некорректное значение {field_name}: должно быть одним из {options}")

        return value


class Sensor(Thing):
    def __init__(self, name, unit="C"):
        super().__init__(name)
        self.unit = unit
        self.value = 0.0
        self.power = "on"
        logger.info(f"Sensor {self.name} initialized with unit {self.unit}")

    def connect(self, command_data):
        response = {"status": "success"}

        try:
            if 'value' in command_data:
                old_value = self.value
                self.value = self.validate_float(command_data['value'], 'value')
                response['value'] = self.value
                logger.info(f"Sensor {self.name} value changed from {old_value} to {self.value}")

            if 'power' in command_data:
                old_power = self.power
                self.power = self.validate_string(command_data['power'], 'power', options=['on', 'off'])
                response['power'] = self.power
                logger.info(f"Sensor {self.name} power changed from {old_power} to {self.power}")

            response['unit'] = self.unit
            return response

        except ValueError as e:
            logger.error(f"Validation error in Sensor {self.name}: {str(e)}")
            return {"status": "error", "message": str(e)}


class Robot(Thing):
    def __init__(self, name):
        super().__init__(name)
        self.status = 0
        self.coordinates = [0, 0]
        self.temperature = 25.0
        self.command_number = 0
        logger.info(f"Robot {self.name} initialized with coordinates {self.coordinates}")

    def connect(self, command_data):
        response = {"status": "success"}

        try:
            if 'status' in command_data:
                old_status = self.status
                self.status = self.validate_int(command_data['status'], 'status')
                response['robot_status'] = self.status
                logger.info(f"Robot {self.name} status changed from {old_status} to {self.status}")

            if 'coordinates' in command_data:
                old_coordinates = self.coordinates
                if not isinstance(command_data['coordinates'], list) or len(command_data['coordinates']) != 2:
                    raise ValueError("Координаты должны быть списком из двух чисел")

                self.coordinates = [
                    self.validate_int(command_data['coordinates'][0], 'coordinate X'),
                    self.validate_int(command_data['coordinates'][1], 'coordinate Y')
                ]
                response['coordinates'] = self.coordinates
                logger.info(f"Robot {self.name} coordinates changed from {old_coordinates} to {self.coordinates}")

            if 'temperature' in command_data:
                old_temp = self.temperature
                self.temperature = self.validate_float(command_data['temperature'], 'temperature')
                response['temperature'] = self.temperature
                logger.info(f"Robot {self.name} temperature changed from {old_temp} to {self.temperature}")

            if 'command_number' in command_data:
                old_cmd = self.command_number
                self.command_number = self.validate_int(command_data['command_number'], 'command_number')
                response['command_number'] = self.command_number
                logger.info(f"Robot {self.name} command number changed from {old_cmd} to {self.command_number}")

            return response

        except ValueError as e:
            logger.error(f"Validation error in Robot {self.name}: {str(e)}")
            return {"status": "error", "message": str(e)}


class MechanicalRobot(Robot):
    def __init__(self, name):
        super().__init__(name)
        self.angle = 0
        self.grab = 0
        logger.info(f"MechanicalRobot {self.name} initialized with angle {self.angle} and grab {self.grab}")

    def connect(self, command_data):
        response = super().connect(command_data)
        if response['status'] != 'success':
            return response

        try:
            if 'angle' in command_data:
                old_angle = self.angle
                self.angle = self.validate_int(command_data['angle'], 'angle')
                if not 0 <= self.angle <= 360:
                    raise ValueError("Угол должен быть между 0 и 360 градусами")
                response['angle'] = self.angle
                logger.info(f"MechanicalRobot {self.name} angle changed from {old_angle} to {self.angle}")

            if 'grab' in command_data:
                old_grab = self.grab
                self.grab = self.validate_int(command_data['grab'], 'grab')
                if self.grab not in [0, 1]:
                    raise ValueError("Захват должен быть 0 (открыт) или 1 (закрыт)")
                response['grab'] = self.grab
                logger.info(f"MechanicalRobot {self.name} grab changed from {old_grab} to {self.grab}")

            return response

        except ValueError as e:
            logger.error(f"Validation error in MechanicalRobot {self.name}: {str(e)}")
            return {"status": "error", "message": str(e)}


class VacuumRobot(Robot):
    SERIAL_PATTERN = re.compile(r'^VAC-\d{4}$')

    def __init__(self, name):
        super().__init__(name)
        self.vacuum_capture = 0  # Инициализируем атрибут
        self.serial_number = "VAC-0000"
        logger.info(
            f"VacuumRobot {self.name} initialized with vacuum capture {self.vacuum_capture} and serial {self.serial_number}")

    def connect(self, command_data):
        response = super().connect(command_data)
        if response['status'] != 'success':
            return response

        try:
            if 'vacuum_capture' in command_data:
                old_capture = self.vacuum_capture
                self.vacuum_capture = self.validate_int(command_data['vacuum_capture'], 'vacuum_capture')
                if self.vacuum_capture not in [0, 1]:
                    error_msg = "Вакуумный захват должен быть 0 (выключен) или 1 (включен)"
                    logger.error(f"Validation error in VacuumRobot {self.name}: {error_msg}")
                    raise ValueError(error_msg)
                response['vacuum_capture'] = self.vacuum_capture
                logger.info(
                    f"VacuumRobot {self.name} vacuum capture changed from {old_capture} to {self.vacuum_capture}")

            if 'serial_number' in command_data:
                if not self.SERIAL_PATTERN.match(command_data['serial_number']):
                    error_msg = "Некорректный серийный номер. Должен быть в формате: VAC-1234"
                    logger.error(f"Validation error in VacuumRobot {self.name}: {error_msg}")
                    raise ValueError(error_msg)
                old_serial = self.serial_number
                self.serial_number = command_data['serial_number']
                response['serial_number'] = self.serial_number
                logger.info(f"VacuumRobot {self.name} serial number changed from {old_serial} to {self.serial_number}")

            return response

        except ValueError as e:
            logger.error(f"Validation error in VacuumRobot {self.name}: {str(e)}")
            return {"status": "error", "message": str(e)}


class SignalLamp(Thing):
    def __init__(self, name, color="red"):
        super().__init__(name)
        self.color = color
        self.power = "on"
        logger.info(f"SignalLamp {self.name} initialized with color {self.color}")

    def connect(self, command_data, COLOR_PATTERN=None):
        response = {"status": "success"}

        try:
            if 'color' in command_data:
                old_color = self.color
                # Проверяем цвет либо по списку, либо как HEX-код
                if command_data['color'].startswith('#'):
                    self.color = self.validate_string(command_data['color'], 'color', COLOR_PATTERN)
                else:
                    self.color = self.validate_string(command_data['color'], 'color',
                                                      options=['Красный', 'Зелёный', 'Синий', 'Жёлтый'])
                response['color'] = self.color
                logger.info(f"SignalLamp {self.name} color changed from {old_color} to {self.color}")

            if 'power' in command_data:
                old_power = self.power
                self.power = self.validate_string(command_data['power'], 'power', options=['on', 'off'])
                response['power'] = self.power
                logger.info(f"SignalLamp {self.name} power changed from {old_power} to {self.power}")

            return response

        except ValueError as e:
            logger.error(f"Validation error in SignalLamp {self.name}: {str(e)}")
            return {"status": "error", "message": str(e)}


# === Обогреватель ===
class Heater(Thing):
    def __init__(self, name, switch_on_temperature=25.0):
        super().__init__(name)
        self.power = "off"
        self.switch_on_temperature = switch_on_temperature
        logger.info(f"Heater {self.name} initialized with switch temperature {self.switch_on_temperature}")

    def connect(self, command_data):
        response = {"status": "success"}

        try:
            if 'power' in command_data:
                old_power = self.power
                self.power = self.validate_string(command_data['power'], 'power', options=['on', 'off'])
                response['power'] = self.power
                logger.info(f"Heater {self.name} power changed from {old_power} to {self.power}")

            return response

        except ValueError as e:
            logger.error(f"Validation error in Heater {self.name}: {str(e)}")
            return {"status": "error", "message": str(e)}

    def auto_power(self, temperature):
        """Автоматическое управление питанием на основе температуры"""
        new_power = "on" if temperature < self.switch_on_temperature else "off"
        if new_power != self.power:
            old_power = self.power
            self.power = new_power
            logger.info(
                f"Heater {self.name} automatically changed power from {old_power} to {self.power} based on temperature {temperature}")
        return self.power
