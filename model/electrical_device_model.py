from abc import ABC, abstractmethod
from utils.enums import TwoStatus as two_status
from utils.enums import ACStatus as ac_status
from utils import config as config

class ElectricalDevice(ABC):
    """Abstract base class for all electrical devices."""
    def __init__(self, device_type, device_id, power_rating, heating_rate):
        if not device_type or not isinstance(device_type, str):
            raise ValueError("Device type must be a non-empty string.")
        if device_id is None or not isinstance(device_id, (int, str)):
            raise ValueError("Device ID must be a valid integer or string.")
        self.device_type = device_type
        self.device_id = device_id
        self.device_full_name = f"{self.device_type} {self.device_id}"
        self.power_rating = 0
        self.heating_rate = 0
        self.status = 0

    @abstractmethod
    def switch_up(self):
        pass

    @abstractmethod
    def switch_down(self):
        pass

    @abstractmethod
    def adjust_power_and_heating(self, status):
        pass


class TwoStatusDevice(ElectricalDevice):
    def switch_up(self):
        
        self.status = 1
        self.adjust_power_and_heating(self.status)

    def switch_down(self):
        
        self.status = 0
        self.adjust_power_and_heating(self.status)

    def adjust_power_and_heating(self, status):
        """Adjust power rating and heating rate based on ON/OFF status."""
        if status not in (0, 1):
            raise ValueError(f"Invalid status for TwoStatusDevice: {status}")
        if status == 1:  # ON
            if self.device_type not in config.DEVICE_CONFIG:
                raise KeyError(f"Device configuration for '{self.device_type}' not found in config.")
            self.power_rating = config.DEVICE_CONFIG[self.device_type]["power_rating"]
            self.heating_rate = config.DEVICE_CONFIG[self.device_type]["heating_rate"]
        elif status == 0:  # OFF
            self.power_rating = 0
            self.heating_rate = 0

class Television(TwoStatusDevice):
    def __init__(self, device_type="Television", device_id=None, power_rating=config.TELEVISION_POWER, heating_rate=config.TELEVISION_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class Lamp(TwoStatusDevice):
    def __init__(self, device_type="Lamp", device_id=None, power_rating=config.TELEVISION_POWER, heating_rate=config.TELEVISION_POWER):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class BedsideLamp(TwoStatusDevice):
    def __init__(self, device_type="Bedside Lamp", device_id=None, power_rating=config.BEDSIDE_LAMP_POWER, heating_rate=config.BEDSIDE_LAMP_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class Refrigerator(TwoStatusDevice):
    def __init__(self, device_type="Refrigerator", device_id=None, power_rating=config.REFRIGERATOR_POWER, heating_rate=config.REFRIGERATOR_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class ElectricKettle(TwoStatusDevice):
    def __init__(self, device_type="Electric Kettle", device_id=None, power_rating=config.ELECTRIC_KETTLE_POWER, heating_rate=config.ELECTRIC_KETTLE_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class AirConditioner(ElectricalDevice):
    def __init__(self, device_type="Air Conditioner", device_id=None, power_rating=0, heating_rate=0):
        super().__init__(device_type, device_id, power_rating, heating_rate)

    def switch_up(self):
        if self.status >= ac_status.AC_MAX_LEVEL.value:
            
            return
        else:
            self.status = self.status + 1
            self.adjust_power_and_heating(self.status)

    def switch_down(self):
        if self.status <= ac_status.AC_MIN_LEVEL.value:
            
            return
        else:
            self.status = self.status - 1
            self.adjust_power_and_heating(self.status)

    def adjust_power_and_heating(self, status):
        """Adjust power rating and heating rate based on AC level."""
        if isinstance(status, int):  # Convert integers to ACStatus if needed
            status = ac_status(status)

        if status in config.AIR_CONDITIONER_CONFIG:
            config_values = config.AIR_CONDITIONER_CONFIG[status]
            self.power_rating = config_values["power"]
            self.heating_rate = config_values["heating_rate"]
        else:
            raise ValueError(f"Invalid status: {status}")