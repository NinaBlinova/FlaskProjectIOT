from abc import ABC, abstractmethod

class Thing(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_status(self):
        pass

class Sensor(Thing):
    def __init__(self, name, value=0):
        super().__init__(name)
        self.value = value

    def get_status(self):
        return f"Sensor {self.name}: {self.value}"

    def update_value(self, new_value):
        self.value = new_value
        print(f"[LOG] {self.name} updated to {self.value}")

class SignalLamp(Thing):
    def __init__(self, name, color="red"):
        super().__init__(name)
        self.color = color

    def get_status(self):
        return f"SignalLamp {self.name} is {self.color}"

    def change_color(self, new_color):
        self.color = new_color
        print(f"[LOG] {self.name} changed to {self.color}")
