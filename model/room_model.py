"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          room_model.py                                                   *
* Purpose:       Implements the Room and derived classes for managing rooms and  *
*                their devices. Controls temperature updates and devices' states.*
* Description:   This file contains the Room class, which manages room devices,  *
*                AC state transitions, temperature updates, and device limits.   *
*                Includes specific room types like Kitchen, LivingRoom, Bedroom. *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o *
*                ChatGPT provided insights on threading, finite state machines,  *
*                and object-oriented design for managing devices in rooms.       *
**********************************************************************************
"""

#********************************** IMPORT ***************************************
# Standard library imports
import threading
import time

# Application-specific imports
from utils.enums import RoomType, TwoStatus as two_status
import utils.config as config 
from utils.config import VALID_DEVICES, MAX_QUANTITY
import model.electrical_device_model as elec_app

#**************************** CLASS DEFINITIONS **********************************

class Room:

    """
    Base class for a room, handling devices, temperature updates, and AC state transitions.
    
    Responsibilities:
    - Manages devices in the room, including adding and removing devices.
    - Tracks and updates room temperature based on total device heat rate.
    - Controls the finite state machine for the center AC system.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes the Room with room type, ID, and default parameters.
    # Input:       room_type (str), room_id (int)
    # Output:      None
    # GPT Prompt:  "How can I design a class in Python that initializes default values
    #               and starts a background thread for continuous updates?"
    # ------------------------------------------------------------------------------        
    def __init__(self, room_type, room_id):
        self.type = room_type
        self.id = room_id
        self.devices = []
        self.total_heat_rate = self.update_total_heat_rate()
        self.center_ac_states = {"TURN_OFF": 1, "COOLING": 2, "HEATING": 3}
        self.current_ac_state = "TURN_OFF"  # Start at TURN_OFF
        self.temperature = config.ROOM_START_TEMPERATURE  # Initial temperature

        # This is a function table for center Air Conditioner finite state machine
        self.center_ac_states_transitions = {
            "TURN_OFF": lambda temp: "TURN_OFF" if config.TEMPERATURE_LOWEER_BOUND <= temp < config.TEMPERATURE_UPPER_BOUND else "COOLING" if temp >= config.TEMPERATURE_UPPER_BOUND else "HEATING",
            "COOLING": lambda temp: "TURN_OFF" if config.TEMPERATURE_LOWEER_BOUND <= temp < config.TEMPERATURE_AVERAGE else "COOLING" if temp >= config.TEMPERATURE_AVERAGE else "HEATING",
            "HEATING": lambda temp: "TURN_OFF" if config.TEMPERATURE_AVERAGE <= temp < config.TEMPERATURE_UPPER_BOUND else "COOLING" if config.TEMPERATURE_UPPER_BOUND <= temp else "HEATING",
        }

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self.update_room_temperature, daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------------------
    # Function:    add_device
    # Description: Adds a new device to the room if it satisfies device limits.
    # Input:       device_type (str)
    # Output:      device object or raises ValueError
    # GPT Prompt:  "How can I validate input and dynamically create class objects
    #               based on a condition in Python?"
    # ------------------------------------------------------------------------------
    def add_device(self, device_type):
        if device_type not in self.valid_devices:
            raise ValueError(f"{device_type} is not allowed in {self.type}.")
        if len([d for d in self.devices if d.device_type == device_type]) >= self.max_quantity.get(device_type, 0):
            raise ValueError(f"Cannot add more {device_type} to {self.type}. Maximum limit reached.")
        
        # Calculate the number of existing tabs with the same type
        same_type_number = sum(1 for device in self.devices if device.device_type == device_type) + 1  # Start with 1

        if device_type == "Television":
            new_device = elec_app.Television(device_type, same_type_number)
        elif device_type == "Lamp":
            new_device = elec_app.Lamp(device_type, same_type_number)
        elif device_type == "Refrigerator":
            new_device = elec_app.Refrigerator(device_type, same_type_number)
        elif device_type == "Bedside Lamp":
            new_device = elec_app.BedsideLamp(device_type, same_type_number)
        elif device_type == "Air Conditioner":
            new_device = elec_app.AirConditioner(device_type, same_type_number)
        elif device_type == "Electric Kettle":
            new_device = elec_app.ElectricKettle(device_type, same_type_number)
        else:
            return ValueError(f"Invalid device: {device_type}")
        # 
        self.devices.append(new_device)
        return new_device

    # ------------------------------------------------------------------------------
    # Function:    remove_current_device
    # Description: Removes a specific device from the room.
    # Input:       device_full_name (str)
    # Output:      None or raises ValueError.
    # GPT Prompt:  "How can I remove a specific item from a list of objects in Python 
    #               based on a unique identifier?"
    # ------------------------------------------------------------------------------    
    def remove_current_device(self, device_full_name):
        """Remove the device of a specific type with the largest ID number."""
        try:
            
            # Find all devices of the specified type
            device_to_remove = next((device for device in self.devices if device.device_full_name == device_full_name), None)
            if not device_to_remove:
                raise ValueError(f"No device '{device_to_remove}' found in {self.type} {self.id}.")
            
            # Check if any device exists for the given type
            device_type_to_remove = device_to_remove.device_type
            devices_to_remove = [device for device in self.devices if device.device_type == device_type_to_remove]
            if not devices_to_remove:
                raise ValueError(f"No devices '{devices_to_remove}' found in {self.type} {self.id}.")

            # Find the device with the largest ID
            device_with_largest_id = max(devices_to_remove, key=lambda d: d.device_id)

            # Remove the device
            self.devices.remove(device_with_largest_id)
            self.update_total_heat_rate()
            return

        except ValueError as e:
            raise ValueError(f"Failed to remove device: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while removing the device: {str(e)}")

    # ------------------------------------------------------------------------------
    # Function:    get_devices_info
    # Description: Retrieves information about all devices in the room, 
    #              including their full names and statuses.
    # Input:       None
    # Output:      List of tuples (device_full_name, status).
    # GPT Prompt:  "How can I retrieve specific attributes from objects in a list and 
    #               format them as tuples in Python?"
    # ------------------------------------------------------------------------------ 
    def get_devices_info(self):
        devices_info = []
        for device in self.devices:
            device_info = (device.device_full_name, device.status)
            devices_info.append(device_info)
        return devices_info

    # ------------------------------------------------------------------------------
    # Function:    get_room_temperature
    # Description: Returns the current temperature of the room.
    # Input:       None
    # Output:      Float representing the room temperature.
    # GPT Prompt:  "How can I retrieve and return a specific attribute from a class in Python?"
    # ------------------------------------------------------------------------------    
    def get_room_temperature(self):
        return self.temperature

    # ------------------------------------------------------------------------------
    # Function:    change_device_state
    # Description: Changes the state of a specified device in the room by switching 
    #              it "UP" or "DOWN", and updates the total heat rate accordingly.
    # Input:       device_full_name (str) - The full name of the device to modify.
    #              direction (str) - The desired state change ("UP" or "DOWN").
    # Output:      None
    # GPT Prompt:  "How can I iterate through a list of objects, match a specific attribute, 
    #               and call a method conditionally based on another parameter?"
    # ------------------------------------------------------------------------------
    def change_device_state(self, device_full_name, direction):

        for device in self.devices:
            if device.device_full_name == device_full_name:
                if direction == "UP":
                    device.switch_up()
                else:
                    device.switch_down()
        self.update_total_heat_rate()
        
    # ------------------------------------------------------------------------------
    # Function:    update_total_heat_rate
    # Description: Updates the cumulative heat rate based on active devices.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I efficiently calculate the sum of a specific attribute 
    #               across a list of objects in Python?"
    # ------------------------------------------------------------------------------
    def update_total_heat_rate(self):
        total_heat_rate = 0
        for device in self.devices:
            total_heat_rate += device.heating_rate
        self.total_heat_rate = total_heat_rate
        return total_heat_rate

    # ------------------------------------------------------------------------------
    # Function:    update_room_temperature
    # Description: Continuously updates the room temperature based on device heat rate.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I implement a background thread in Python to simulate periodic 
    #               updates, such as temperature changes in a room?"
    # ------------------------------------------------------------------------------
    def update_room_temperature(self):
        while not self._stop_event.is_set():
            self.current_ac_state = self.center_ac_states_transitions[self.current_ac_state](self.temperature)

            if self.current_ac_state == "TURN_OFF":
                self.temperature += config.TEMPERATURE_CHANGE_HEATING_RATE_CONSTANT * self.total_heat_rate * config.TEMPERATURE_CHANGE_REFRESH_RATE

            elif self.current_ac_state == "COOLING":
                self.temperature -= config.CENTER_AIR_CONDITIONER_TEMPERATURE_CHANGE_RATE

            elif self.current_ac_state == "HEATING":
                self.temperature += config.CENTER_AIR_CONDITIONER_TEMPERATURE_CHANGE_RATE

            else:
                raise ValueError(f"Center AC state: {self.current_ac_state} is not defined")
            time.sleep(config.TEMPERATURE_CHANGE_REFRESH_RATE)

    # ------------------------------------------------------------------------------
    # Function:    stop_thread
    # Description: Safely stops the background thread responsible for updating the 
    #              room temperature by setting a stop event and joining the thread.
    # Input:       None
    # Output:      None
    # Exceptions:  Raises ValueError if an error occurs during the thread stop process.
    # GPT Prompt:  "How can I safely stop a running thread in Python using threading 
    #               events and join the thread without causing deadlocks?"
    # ------------------------------------------------------------------------------
    def stop_thread(self):
        try:
            self._stop_event.set()
            self._thread.join()
            return
        except ValueError as e:
            raise ValueError(str(e))

#**************************** CLASS DEFINITIONS **********************************

# IMPORTANT: DO NOT COMBINE THE DERIVATED CLASSES AS THEY WILL BE MODIFIED IN NEXT
#            VERSION
class Kitchen(Room):

    """
    Subclass of Room, representing a Kitchen.
    
    Responsibilities:
    - Defines the valid devices that can be added to a kitchen.
    - Sets the maximum quantity constraints for each device type.
    - Inherits room temperature management and device handling from the Room class.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes a Kitchen room with valid devices and max constraints.
    # Input:       room_id (int) - Unique identifier for the Kitchen.
    # Output:      None
    # GPT Prompt:  "How can I create a Python subclass that defines constraints 
    #              for specific device types while inheriting base class methods?"
    # ------------------------------------------------------------------------------    
    def __init__(self, room_id):
        super().__init__(room_type=RoomType.KITCHEN.value, room_id=room_id)
        self.valid_devices = VALID_DEVICES[RoomType.KITCHEN]
        self.max_quantity = MAX_QUANTITY[RoomType.KITCHEN]

class LivingRoom(Room):

    """
    Subclass of Room, representing a Living Room.
    
    Responsibilities:
    - Defines the valid devices that can be added to a living room.
    - Sets the maximum quantity constraints for each device type.
    - Inherits room temperature management and device handling from the Room class.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes a Living Room with valid devices and max constraints.
    # Input:       room_id (int) - Unique identifier for the Living Room.
    # Output:      None
    # GPT Prompt:  "How do I extend a parent class in Python to customize attributes 
    #              for specific subclasses like a Living Room?"
    # ------------------------------------------------------------------------------
    def __init__(self, room_id):
        super().__init__(room_type=RoomType.LIVING_ROOM.value, room_id=room_id)
        self.valid_devices = VALID_DEVICES[RoomType.LIVING_ROOM]
        self.max_quantity = MAX_QUANTITY[RoomType.LIVING_ROOM]

class Bedroom(Room):

    """
    Subclass of Room, representing a Bedroom.
    
    Responsibilities:
    - Defines the valid devices that can be added to a bedroom.
    - Sets the maximum quantity constraints for each device type.
    - Inherits room temperature management and device handling from the Room class.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes a Bedroom with valid devices and max constraints.
    # Input:       room_id (int) - Unique identifier for the Bedroom.
    # Output:      None
    # GPT Prompt:  "How can I design a Python subclass that restricts device types 
    #              and quantities while extending base class methods?"
    # ------------------------------------------------------------------------------
    def __init__(self, room_id):
        super().__init__(room_type=RoomType.BEDROOM.value, room_id=room_id)
        self.valid_devices = VALID_DEVICES[RoomType.BEDROOM]
        self.max_quantity = MAX_QUANTITY[RoomType.BEDROOM]