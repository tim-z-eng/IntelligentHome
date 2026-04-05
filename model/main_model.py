"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          main_model.py                                                   *
* Purpose:       Implements the MainModel, WelcomeModel, RoomTabModel, and       *
*                TabModel classes for managing tabs, rooms, and devices.         *
* Description:   Handles saving/loading tabs, managing room tabs, devices, and   *
*                room temperature. Supports dynamic device addition, removal,    *
*                and state changes.                                              *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o *
*                ChatGPT provided insights on data persistence, JSON handling,   *
*                mapping constructors, and state management techniques.          *
**********************************************************************************
"""

#********************************** IMPORT ***************************************
# Standard library imports
import json
import os

# Application-specific imports
from utils.config import WELCOME_MESSAGE
from utils.enums import RoomType

# Room and Device Models
from model.room_model import Room, Kitchen, LivingRoom, Bedroom
from model.electrical_device_model import (
    Television, Lamp, BedsideLamp, Refrigerator, ElectricKettle, AirConditioner
)

# Abstract Base Class
from abc import ABC, abstractmethod

#********************************** CONSTANTS ************************************

# Mapping of room types to constructors
ROOM_TYPE_MAPPING = {
    RoomType.KITCHEN.value: Kitchen,
    RoomType.LIVING_ROOM.value: LivingRoom,
    RoomType.BEDROOM.value: Bedroom,
}

# Mapping of device types to constructors
DEVICE_TYPE_MAPPING = {
    "Television": Television,
    "Lamp": Lamp,
    "Bedside Lamp": BedsideLamp,
    "Refrigerator": Refrigerator,
    "Electric Kettle": ElectricKettle,
    "Air Conditioner": AirConditioner,
}

#****************************** CLASS DEFINITIONS *********************************

class MainModel:

    """
    A class to manage tabs, rooms, and devices in the IntelligentHome system.
    
    Responsibilities:
    - Load and save tabs from/to JSON files.
    - Manage room tabs and their devices.
    - Support dynamic operations like adding/removing devices and changing states.
    """
    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes the MainModel class and loads existing tabs from JSON.
    # Input:       None
    # Output:      Initialized MainModel instance with self.tabs.
    # GPT Prompt:  "How can I load and manage JSON data in Python with error handling?"
    # ------------------------------------------------------------------------------    
    def __init__(self):

        """Initialize the RoomModel class."""

        self.db_path = os.path.join("database", "tabs.json")
        self.tabs = [] # Protected variable
        self.current_tab = None
        self.load_tabs()

    # ------------------------------------------------------------------------------
    # Function:    load_tabs
    # Description: Loads tab data from the JSON file. Adds a default Welcome tab.
    # Input:       JSON file (self.db_path)
    # Output:      Updated self.tabs list.
    # GPT Prompt:  "How can I load structured JSON data into Python objects while handling errors?"
    # ------------------------------------------------------------------------------
    # IMPORTANT: DO NOT EVER THINK ABOUT TOUCHING THIS METHOD
    #            IT TAKES HOURS TO FIX THIS LOAD METHOD
    def load_tabs(self):

        """Load tabs from the JSON file."""

        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as file:
                    data = json.load(file)  # Load JSON data
                    if isinstance(data, list):  # Ensure the data is a list
                        self.tabs = []
                        
                        for tab_data in data:
                            tab_type = tab_data.get("tab_type")
                            tab_id = tab_data.get("tab_id")
                            room_data = tab_data.get("room")

                            if tab_type in ROOM_TYPE_MAPPING:
                                room_class = ROOM_TYPE_MAPPING[tab_type]
                                room = room_class(room_id=room_data.get("id"))

                                for device_data in room_data.get("devices", []):
                                    device_type = device_data.get("device_type")
                                    device_id = device_data.get("device_id")
                                    if device_type in DEVICE_TYPE_MAPPING:
                                        device_class = DEVICE_TYPE_MAPPING[device_type]
                                        room.devices.append(device_class(device_id=device_id))
                                    else:
                                        raise ValueError(f"Unknown device type: {device_type}")

                                self.tabs.append(RoomTabModel(tab_type, tab_id, room))
                    else:
                        self.tabs = []  # Reinitialize tabs
                        self.save_tabs()  # Save an empty list
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                self.tabs = []  # Reinitialize tabs
                self.save_tabs()  # Save an empty list
        else:
            
            # File doesn't exist; create an empty tabs file
            self.tabs = []
            self.save_tabs()
        
        self.tabs.insert(0, WelcomeModel("Welcome", 0, WELCOME_MESSAGE))

    # ------------------------------------------------------------------------------
    # Function:    save_tabs
    # Description: Saves current tabs and their data to a JSON file.
    # Input:       Current state of self.tabs.
    # Output:      JSON file (self.db_path) updated with tab data.
    # GPT Prompt:  "How do I write structured data to a JSON file in Python?"
    # ------------------------------------------------------------------------------
    # IMPORTANT: DO NOT EVER THINK ABOUT TOUCHING THIS METHOD
    #            IT TAKES HOURS TO FIX THIS SAVE METHOD
    def save_tabs(self):

        """Save the current tabs list to a JSON file."""
        
        # Prepare data for saving
        data = []
        for tab in self.tabs[1:]:  # Skip the Welcome tab
            if isinstance(tab, RoomTabModel) and tab.room:  # Only RoomTabModel has 'room'
                room_devices = [{"device_type": device.device_type, "device_id": device.device_id} for device in tab.room.devices]

                data.append({
                    "tab_type": tab.tab_type,
                    "tab_id": tab.tab_id,
                    "room": {
                        "type": tab.room.type,
                        "id": tab.room.id,
                        "devices": room_devices
                    }
                })
            else:
                
                # Save generic TabModel or other types
                data.append({
                    "tab_type": tab.tab_type,
                    "tab_id": tab.tab_id
                })
    
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    # ------------------------------------------------------------------------------
    # Function:    add_tab
    # Description: Adds a new tab of the specified type.
    # Input:       tab_type (str) - Type of the tab (e.g., 'Kitchen', 'Living Room').
    # Output:      Newly created tab instance.
    # GPT Prompt:  "How can I dynamically create and manage Python objects based on type mappings?"
    # ------------------------------------------------------------------------------
    def add_tab(self, tab_type):

        """Add a new tab to the application based on the tab type."""

        # Validate tab_type
        if not tab_type or not isinstance(tab_type, str):
            raise ValueError("Tab type must be a non-empty string.")

        # Check if tab_type is valid
        if tab_type != "Welcome" and tab_type not in ROOM_TYPE_MAPPING:
            raise ValueError(f"Invalid tab type: {tab_type}. Allowed types: 'Welcome', {list(ROOM_TYPE_MAPPING.keys())}")

        # Calculate the number of existing tabs with the same type
        same_type_number = sum(1 for tab in self.tabs if tab.tab_type == tab_type) + 1

        # Create the tab based on its type
        if tab_type == "Welcome":
            # Ensure only one Welcome tab exists
            if any(tab.tab_type == "Welcome" for tab in self.tabs):
                raise ValueError("A Welcome tab already exists. Cannot add another.")
            new_tab = WelcomeModel(tab_type, same_type_number, WELCOME_MESSAGE)
        else:
            # Create a RoomTabModel for specific room types
            room_class = ROOM_TYPE_MAPPING[tab_type]
            new_room = room_class(room_id=same_type_number)
            new_tab = RoomTabModel(tab_type, same_type_number, new_room)

        # Add the new tab to the list and save
        self.tabs.append(new_tab)
        self.save_tabs()

        return new_tab

     # ------------------------------------------------------------------------------
    # Function:    add_device
    # Description: Adds a new device to a specific room tab.
    # Input:       tab_to_be_added_on_name (str), device_type (str)
    # Output:      tuple: (success (bool), message (str))
    # GPT Prompt:  "How can I dynamically add an object to a list of objects in Python?"
    # ------------------------------------------------------------------------------   
    def add_device(self, tab_to_be_added_on_name, device_type):

        """Add a new device to a specific tab (room)."""

        try:
            # Find the tab by its full name
            for tab in self.tabs:
                if tab.tab_full_name == tab_to_be_added_on_name:
                    # Ensure the tab is a RoomTabModel
                    if not isinstance(tab, RoomTabModel):
                        
                        return False, f"{tab_to_be_added_on_name} is not a valid room tab."

                    # Add the device to the room
                    new_device = tab.add_device_to_room(device_type)
                    
                    return True, f"Device {new_device.device_type} added successfully to {tab_to_be_added_on_name}."
        
            # Tab not found
            return False, f"Tab '{tab_to_be_added_on_name}' not found."

        except ValueError as e:
            
            # Handle any errors raised during device addition
            raise ValueError(str(e))

    # ------------------------------------------------------------------------------
    # Function:    remove_current_device
    # Description: Removes a specific device from a room tab.
    # Input:       tab_full_name (str), device_full_name (str)
    # Output:      tuple: (success (bool), message (str))
    # GPT Prompt:  "How do I search and remove an object from a list based on a condition in Python?"
    # ------------------------------------------------------------------------------        
    def remove_current_device(self, tab_full_name, device_full_name):

        """Remove a selected device to a specific tab (room)."""

        try:
            # Find the tab by its full name
            for tab in self.tabs:
                if tab.tab_full_name == tab_full_name:
                    # Ensure the tab is a RoomTabModel
                    if not isinstance(tab, RoomTabModel):
                        
                        return False, f"{tab_full_name} is not a valid room tab."

                    # Add the device to the room
                    tab.remove_device_from_room(device_full_name)
                    
                    return True, f"Device {device_full_name} removed successfully to {tab_full_name}."
        
            # Tab not found
            return False, f"Tab '{tab_full_name}' not found."

        except ValueError as e:
            
            # Handle any errors raised during device addition
            raise ValueError(str(e))     

    # ------------------------------------------------------------------------------
    # Function:    get_tab_full_names
    # Description: Retrieves the full names of all tabs.
    # Input:       None
    # Output:      List of tab full names.
    # GPT Prompt:  "How can I extract specific attributes from a list of Python objects?"
    # ------------------------------------------------------------------------------
    def get_tab_full_names(self):

        """Return a list of all tab full names in the model."""
        
        return [tab.tab_full_name for tab in self.tabs]

    # ------------------------------------------------------------------------------
    # Function:    get_tab_info
    # Description: Returns detailed information for a specific tab.
    # Input:       tab_full_name (str)
    # Output:      Tuple: (tab name, temperature, devices info)
    # GPT Prompt:  "How can I retrieve specific object attributes by filtering a list in Python?"
    # ------------------------------------------------------------------------------
    def get_tab_info(self, tab_full_name):

        """Return the rooms dictionary."""

        for tab in self.tabs:
            if tab.tab_full_name == tab_full_name:
                
                return tab.get_tab_info()
        raise ValueError(f"Tab full name: {tab_full_name} is invalid")

    # ------------------------------------------------------------------------------
    # Function:    change_device_state
    # Description: Changes the state of a device (e.g., ON/OFF) in a room tab.
    # Input:       tab_full_name (str), device_full_name (str), direction (str)
    # Output:      None
    # GPT Prompt:  "How can I update the attribute of an object dynamically in Python?"
    # ------------------------------------------------------------------------------    
    def change_device_state(self, tab_full_name, device_full_name, direction):

        """Change the state of a device in a specific room."""

        for tab in self.tabs:
            
            if tab.tab_full_name == tab_full_name:
                
                tab.change_device_state(device_full_name, direction)
                return
            
        raise ValueError(f"Tab full name: {tab_full_name} is invalid")

#********************************** CLASS DEFINITIONS *****************************

class TabModel:

    """
    Abstract base class for all tab models.
    
    Responsibilities:
    - Serves as a base class for WelcomeModel and RoomTabModel.
    - Provides common properties like tab type, ID, and full name.
    """
    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes a tab model with a type and optional ID.
    # Input:       tab_type (str), tab_id (int)
    # Output:      None
    # GPT Prompt:  "How can I create a base class in Python with common properties
    #               and methods for subclasses?"
    # ------------------------------------------------------------------------------    
    def __init__(self, tab_type, tab_id=None):
        self.tab_type = tab_type
        self.tab_id = tab_id
        self.tab_full_name = f"{self.tab_type}{tab_id}"

    @abstractmethod
    def get_tab_info(self):
        pass

class WelcomeModel(TabModel):

    """
    A concrete implementation of TabModel for the Welcome tab.
    
    Responsibilities:
    - Manages the Welcome tab, which has a fixed welcome message.
    """
    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes the WelcomeModel with a welcome message.
    # Input:       tab_type (str), tab_id (int), welcome_message (str)
    # Output:      None
    # GPT Prompt:  "How can I subclass an abstract class and override its methods
    #               in Python?"
    # ------------------------------------------------------------------------------    
    def __init__(self, tab_type, tab_id, welcome_message):
        super().__init__(tab_type, tab_id)
        self.tab_full_name = f"{self.tab_type}"
        self.welcome_message = welcome_message

    # ------------------------------------------------------------------------------
    # Function:    get_tab_info
    # Description: Returns information for the Welcome tab.
    # Input:       None
    # Output:      tuple: (tab_full_name, None, None)
    # GPT Prompt:  "How can I override a method in a Python subclass to provide
    #               specific behavior?"
    # ------------------------------------------------------------------------------
    def get_tab_info(self):
        
        return self.tab_full_name, None, None

class RoomTabModel(TabModel):

    """
    A concrete implementation of TabModel for room tabs.
    
    Responsibilities:
    - Manages a specific room and its devices.
    - Supports operations like adding/removing devices and changing device states.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes the RoomTabModel with a room object.
    # Input:       tab_type (str), tab_id (int), room (Room)
    # Output:      None
    # GPT Prompt:  "How can I pass an object to a class constructor in Python
    #               and use it in the class?"
    # ------------------------------------------------------------------------------
    def __init__(self, tab_type, tab_id, room):
        super().__init__(tab_type, tab_id)
        self.room = room

    # ------------------------------------------------------------------------------
    # Function:    get_tab_info
    # Description: Returns the tab name, room temperature, and devices info.
    # Input:       None
    # Output:      tuple: (tab_full_name, room_temperature, devices_info)
    # GPT Prompt:  "How can I return multiple pieces of information from a method
    #               in Python?"
    # ------------------------------------------------------------------------------
    def get_tab_info(self):
        room_temperature = self.room.get_room_temperature()
        devices_info = self.room.get_devices_info()

        return self.tab_full_name, room_temperature, devices_info

    # ------------------------------------------------------------------------------
    # Function:    add_device_to_room
    # Description: Adds a device to the room.
    # Input:       device_type (str)
    # Output:      Device object
    # GPT Prompt:  "How can I dynamically create and add objects to a list in Python?"
    # ------------------------------------------------------------------------------    
    def add_device_to_room(self, device_type):
        """Add a device to the room."""
        return self.room.add_device(device_type)

    # ------------------------------------------------------------------------------
    # Function:    remove_device_from_room
    # Description: Removes a specific device from the room.
    # Input:       device_full_name (str)
    # Output:      None
    # GPT Prompt:  "How do I search and remove an object from a list in Python
    #               based on a condition?"
    # ------------------------------------------------------------------------------
    def remove_device_from_room(self, device_full_name):
        """Remove a device from the room."""
        self.room.remove_current_device(device_full_name)

    # ------------------------------------------------------------------------------
    # Function:    change_device_state
    # Description: Changes the state of a specific device in the room.
    # Input:       device_full_name (str), direction (str)
    # Output:      None
    # GPT Prompt:  "How can I update an object’s property dynamically in Python?"
    # ------------------------------------------------------------------------------    
    def change_device_state(self, device_full_name, direction):

        self.room.change_device_state(device_full_name, direction)

    # ------------------------------------------------------------------------------
    # Function:    stop_thread
    # Description: Stops any background threads in the room (if applicable).
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I gracefully stop background threads in Python classes?"
    # ------------------------------------------------------------------------------
    def stop_thread(self):
        self.room.stop_thread()