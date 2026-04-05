"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          electrical_device_model.py                                      *
* Purpose:       Implements ElectricalDevice base class and its subclasses       *
*                for managing various electrical devices and their states.       *
* Description:   Defines an abstract ElectricalDevice class, concrete device     *
*                classes (e.g., Television, Lamp, AirConditioner), and methods   *
*                for state management, including ON/OFF transitions and power    *
*                adjustments.                                                    *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o *
*                ChatGPT provided insights on Python abstract base classes,      *
*                state transitions, and dynamic attribute handling.              *
**********************************************************************************
"""

#********************************** IMPORT ***************************************

# Standard Library Imports
from abc import ABC, abstractmethod

# Third-Party Imports (None in this case)

# Application-Specific Imports
from utils.enums import TwoStatus as two_status
from utils.enums import ACStatus as ac_status
from utils import config as config

#********************************** CLASS DEFINITION *****************************

class ElectricalDevice(ABC):
    
    """
    Abstract base class for all electrical devices.
    
    Responsibilities:
    - Defines the shared attributes such as device type, ID, power rating, heating rate, and status.
    - Enforces implementation of methods for switching states and adjusting device behavior.
    """

    # --------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes the ElectricalDevice with shared attributes.
    # Input:       device_type (str), device_id (int/str), power_rating (float), heating_rate (float)
    # Output:      None
    # GPT Prompt:  "How can I design a Python abstract base class to enforce method 
    #              implementation while initializing shared attributes for all subclasses?"
    # --------------------------------------------------------------------------
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

    """
    Subclass of ElectricalDevice for devices with two statuses (ON/OFF).
    
    Responsibilities:
    - Implements state transitions for devices that can be turned ON or OFF.
    - Adjusts power rating and heating rate dynamically based on state.
    """
    # --------------------------------------------------------------------------
    # Function:    switch_up
    # Description: Switches the device to the ON state.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I implement a method in Python to change a device status to ON?"
    # --------------------------------------------------------------------------    
    def switch_up(self):
        
        self.status = 1
        self.adjust_power_and_heating(self.status)

    # --------------------------------------------------------------------------
    # Function:    switch_down
    # Description: Switches the device to the OFF state.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I implement a method in Python to change a device status to OFF?"
    # --------------------------------------------------------------------------
    def switch_down(self):
        
        self.status = 0
        self.adjust_power_and_heating(self.status)

    # --------------------------------------------------------------------------
    # Function:    adjust_power_and_heating
    # Description: Adjusts power rating and heating rate based on ON/OFF status.
    # Input:       status (int) - The state of the device (0 or 1)
    # Output:      None
    # GPT Prompt:  "How can I dynamically adjust attributes based on device status in Python?"
    # --------------------------------------------------------------------------
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

    """
    Represents a Television device with two statuses (ON/OFF).
    
    Responsibilities:
    - Sets default power rating and heating rate specific to televisions.
    """

    def __init__(self, device_type="Television", device_id=None, power_rating=config.TELEVISION_POWER, heating_rate=config.TELEVISION_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class Lamp(TwoStatusDevice):

    """
    Represents a Lamp device with two statuses (ON/OFF).
    
    Responsibilities:
    - Sets default power rating and heating rate specific to lamps.
    """

    def __init__(self, device_type="Lamp", device_id=None, power_rating=config.TELEVISION_POWER, heating_rate=config.TELEVISION_POWER):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class BedsideLamp(TwoStatusDevice):

    """
    Represents a Bedside Lamp device with two statuses (ON/OFF).
    
    Responsibilities:
    - Sets default power rating and heating rate specific to bedside lamps.
    """

    def __init__(self, device_type="Bedside Lamp", device_id=None, power_rating=config.BEDSIDE_LAMP_POWER, heating_rate=config.BEDSIDE_LAMP_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class Refrigerator(TwoStatusDevice):

    """
    Represents a Refrigerator device with two statuses (ON/OFF).
    
    Responsibilities:
    - Sets default power rating and heating rate specific to refrigerators.
    """

    def __init__(self, device_type="Refrigerator", device_id=None, power_rating=config.REFRIGERATOR_POWER, heating_rate=config.REFRIGERATOR_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class ElectricKettle(TwoStatusDevice):

    """
    Represents an Electric Kettle device with two statuses (ON/OFF).
    
    Responsibilities:
    - Sets default power rating and heating rate specific to electric kettles.
    """

    def __init__(self, device_type="Electric Kettle", device_id=None, power_rating=config.ELECTRIC_KETTLE_POWER, heating_rate=config.ELECTRIC_KETTLE_HEATING_RATE):
        super().__init__(device_type, device_id, power_rating, heating_rate)

class AirConditioner(ElectricalDevice):

    """
    Represents an Air Conditioner device with multiple states.
    
    Responsibilities:
    - Manages AC level transitions (e.g., cooling and heating modes).
    - Adjusts power rating and heating rate dynamically based on the AC level.
    """

    def __init__(self, device_type="Air Conditioner", device_id=None, power_rating=0, heating_rate=0):
        super().__init__(device_type, device_id, power_rating, heating_rate)

    # --------------------------------------------------------------------------
    # Function:    switch_up
    # Description: Increases the AC level by one step, up to the maximum allowed level.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I implement a method to increase the status of an air conditioner 
    #              while ensuring it does not exceed the maximum allowable value?"
    # --------------------------------------------------------------------------
    def switch_up(self):
        if self.status >= ac_status.AC_MAX_LEVEL.value:
            
            return
        else:
            self.status = self.status + 1
            self.adjust_power_and_heating(self.status)

    # --------------------------------------------------------------------------
    # Function:    switch_down
    # Description: Decreases the AC level by one step, down to the minimum allowed level.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I implement a method to decrease the status of an air conditioner 
    #              while ensuring it does not fall below the minimum allowable value?"
    # --------------------------------------------------------------------------
    def switch_down(self):
        if self.status <= ac_status.AC_MIN_LEVEL.value:
            
            return
        else:
            self.status = self.status - 1
            self.adjust_power_and_heating(self.status)

    # --------------------------------------------------------------------------
    # Function:    adjust_power_and_heating
    # Description: Adjusts the power rating and heating rate of the air conditioner 
    #              based on its current operating level.
    # Input:       status (int): Current status level of the AC.
    # Output:      None
    # GPT Prompt:  "How can I dynamically set power and heating rates for an air conditioner 
    #              based on its operating level in a Python class?"
    # --------------------------------------------------------------------------
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