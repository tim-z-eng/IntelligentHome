"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          config.py                                                       *
* Purpose:       Defines configuration constants for room types, devices, and    *
*                temperature settings used throughout the IntelligentHome system.*
* Description:   Contains constants for window dimensions, UI settings,          *
*                valid devices, maximum quantities, power ratings, heating rates,*
*                and air conditioner configurations.                             *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o.*
*                ChatGPT provided insights on structured configuration design     *
*                and proper mapping of constants for modular code management.    *
**********************************************************************************
"""

from utils.enums import ACStatus
from utils.enums import RoomType
import utils.config as config

# IMPORTANT: THE GUI CONSTANT HAS NOT FULLY IMPLEMENT
#            THIS WILL BE IMPLEMENT IN VERSION 2.0
#            AS THEY CAN BE ADJUSTED IN GUI SETTING

TEXT_PADY = 10 
BUTTON_PADX = 5
BUTTON_PADY = 5 

HEADER_FONT = "Arial"
HEADER_SIZE = 17

LABEL_FONT = "Arial"
LABEL_SIZE = 12
LABEL_PADX = 5
LABEL_PADY = 5

# LOGGIN_WINDOW_WIDTH = 300
# LOGGIN_WINDOW_HEIGHT = 400
WELCOME_MESSAGE = "Welcome to Intelligent Room"

POPUP_WINDOW_WIDTH = 300
POPUP_WINDOW_HEIGHT = 400


#********************************** LOGIN WINDOW CONSTANTS ************************

# General Window Dimensions
LOGIN_WINDOW_WIDTH = 300                        # Width of the login window
LOGIN_WINDOW_HEIGHT = 400                       # Height of the login window
LOGIN_WINDOW_MAIN_FRAME_PAD = "25 25 20 20"

# Title Settings
LOGIN_TITLE_FONT = "Arial"                      # Font for the login title
LOGIN_TITLE_SIZE = 17                           # Font size for the login title
LOGIN_TITLE_PADY = 5                            # Vertical padding for the login title

# Logo Settings
LOGIN_LOGO_WIDTH = 80                           # Width of the UBC logo
LOGIN_LOGO_HEIGHT = 100                         # Height of the UBC logo
LOGIN_LOGO_PADX = 20                            # Horizontal padding for the logo
LOGIN_LOGO_PADY = 20                            # Vertical padding for the logo
LOGIN_LOGO_RESAMPLE_METHOD = "LANCZOS"          # Resampling method for logo scaling

# Username Label
LOGIN_USERNAME_LABEL_TEXT = "Username"          # Text for the username label
LOGIN_USERNAME_LABEL_FONT = "Arial"             # Font for the username label
LOGIN_USERNAME_LABEL_SIZE = 12                  # Font size for the username label
LOGIN_USERNAME_LABEL_PADX = 5                  # Horizontal padding for the username label
LOGIN_USERNAME_LABEL_PADY = 5                   # Vertical padding for the username label

# Username Entry
LOGIN_USERNAME_ENTRY_WIDTH = 20                 # Width for the username entry field
LOGIN_USERNAME_ENTRY_PADX = 5                  # Horizontal padding for the username entry
LOGIN_USERNAME_ENTRY_PADY = 5                   # Vertical padding for the username entry

# Password Label
LOGIN_PASSWORD_LABEL_TEXT = "Password"          # Text for the password label
LOGIN_PASSWORD_LABEL_FONT = "Arial"             # Font for the password label
LOGIN_PASSWORD_LABEL_SIZE = 12                  # Font size for the password label
LOGIN_PASSWORD_LABEL_PADX = 5                  # Horizontal padding for the password label
LOGIN_PASSWORD_LABEL_PADY = 5                   # Vertical padding for the password label

# Password Entry
LOGIN_PASSWORD_ENTRY_WIDTH = 20                 # Width for the password entry field
LOGIN_PASSWORD_ENTRY_PADX = 5                  # Horizontal padding for the password entry
LOGIN_PASSWORD_ENTRY_PADY = 5                   # Vertical padding for the password entry

# Login Button
LOGIN_BUTTON_TEXT = "Login"                     # Text for the login button
LOGIN_BUTTON_WIDTH = 20                         # Width of the login button
LOGIN_BUTTON_PADY = 5                           # Vertical padding for the login button

# Add Admin Button
LOGIN_ADD_ADMIN_BUTTON_TEXT = "Add Admin"       # Text for the add admin button
LOGIN_ADD_ADMIN_BUTTON_WIDTH = 20               # Width of the add admin button
LOGIN_ADD_ADMIN_BUTTON_PADY = 5                # Vertical padding for the add admin button

# Add User Button
LOGIN_ADD_USER_BUTTON_TEXT = "Add User"         # Text for the add user button
LOGIN_ADD_USER_BUTTON_WIDTH = 20                # Width of the add user button
LOGIN_ADD_USER_BUTTON_PADY = 5                 # Vertical padding for the add user button

#********************************** REGISTER WINDOW CONSTANTS *********************

# General Window Dimensions
REGISTER_WINDOW_WIDTH = 300                     # Width of the register window
REGISTER_WINDOW_HEIGHT = 400                    # Height of the register window


#********************************** ROOM AND DEVICE CONFIG ************************

# Valid Devices for Each Room
VALID_DEVICES = {
    RoomType.KITCHEN: ["Air Conditioner", "Refrigerator", "Electric Kettle"],
    RoomType.LIVING_ROOM: ["Air Conditioner", "Television", "Lamp"],
    RoomType.BEDROOM: ["Air Conditioner", "Bedside Lamp", "Television"],
}

# Maximum Quantities for Devices in Each Room
MAX_QUANTITY = {
    RoomType.KITCHEN: {
        "Air Conditioner": 1,
        "Refrigerator": 2,
        "Microwave": 3,
        "Electric Kettle": 4,
    },
    RoomType.LIVING_ROOM: {
        "Air Conditioner": 1,
        "Television": 4,
        "Lamp": 4,
        "Ceiling Fan": 10,
    },
    RoomType.BEDROOM: {
        "Air Conditioner": 1,
        "Bedside Lamp": 3,
        "Television": 3,
    },
}

# Temperature Setting
ROOM_START_TEMPERATURE = 25
TEMPERATURE_UPPER_BOUND = 30
TEMPERATURE_LOWEER_BOUND = 20
TEMPERATURE_AVERAGE = 25

# Heating rate and center Air Conditioner Setting
TEMPERATURE_CHANGE_HEATING_RATE_CONSTANT = 0.001
TEMPERATURE_CHANGE_REFRESH_RATE = 1.0
CENTER_AIR_CONDITIONER_TEMPERATURE_CHANGE_RATE = 0.3

# Power ratings (in Watts)
TELEVISION_POWER = 120
AIR_CONDITIONER_POWER_OFF = 0
AIR_CONDITIONER_POWER_START = 0
AIR_CONDITIONER_POWER_Level_1 = 500
AIR_CONDITIONER_POWER_Level_2 = 750
AIR_CONDITIONER_POWER_Level_3 = 1000
AIR_CONDITIONER_POWER_Level_4 = 1250
AIR_CONDITIONER_POWER_Level_5 = 1500
LAMP_POWER = 60
CEILING_FAN_POWER = 70
BEDSIDE_LAMP_POWER = 40
REFRIGERATOR_POWER = 300
ELECTRIC_KETTLE_POWER = 1500

# Heating rates (in Watts)
TELEVISION_HEATING_RATE = 50
AIR_CONDITIONER_HEATING_RATE_Level_N1 = -100
AIR_CONDITIONER_HEATING_RATE_Level_N2 = -175
AIR_CONDITIONER_HEATING_RATE_Level_N3 = -250
AIR_CONDITIONER_HEATING_RATE_Level_N4 = -325
AIR_CONDITIONER_HEATING_RATE_Level_N5 = -400
AIR_CONDITIONER_HEATING_RATE_OFF = 0
AIR_CONDITIONER_HEATING_RATE_START = 0
AIR_CONDITIONER_HEATING_RATE_Level_P1 = 150
AIR_CONDITIONER_HEATING_RATE_Level_P2 = 750
AIR_CONDITIONER_HEATING_RATE_Level_P3 = 1000
AIR_CONDITIONER_HEATING_RATE_Level_P4 = 1250
AIR_CONDITIONER_HEATING_RATE_Level_P5 = 1500
LAMP_HEATING_RATE = 30
CEILING_FAN_HEATING_RATE = 70
BEDSIDE_LAMP_HEATING_RATE = 12
REFRIGERATOR_HEATING_RATE = 45
ELECTRIC_KETTLE_HEATING_RATE = 150

# Air Conditioner Level Mapping
AIR_CONDITIONER_CONFIG = {
    ACStatus.COOLING_LEVEL_1: {
        "power": config.AIR_CONDITIONER_POWER_Level_1,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_N1,
    },
    ACStatus.COOLING_LEVEL_2: {
        "power": config.AIR_CONDITIONER_POWER_Level_2,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_N2,
    },
    ACStatus.COOLING_LEVEL_3: {
        "power": config.AIR_CONDITIONER_POWER_Level_3,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_N3,
    },
    ACStatus.COOLING_LEVEL_4: {
        "power": config.AIR_CONDITIONER_POWER_Level_4,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_N4,
    },
    ACStatus.COOLING_LEVEL_5: {
        "power": config.AIR_CONDITIONER_POWER_Level_5,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_N5,
    },
    ACStatus.OFF: {
        "power": config.AIR_CONDITIONER_POWER_OFF,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_OFF,
    },
    ACStatus.AC_START: {
        "power": config.AIR_CONDITIONER_POWER_START,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_START,
    },
    ACStatus.HEATING_LEVEL_1: {
        "power": config.AIR_CONDITIONER_POWER_Level_1,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_P1,
    },
    ACStatus.HEATING_LEVEL_2: {
        "power": config.AIR_CONDITIONER_POWER_Level_2,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_P2,
    },
    ACStatus.HEATING_LEVEL_3: {
        "power": config.AIR_CONDITIONER_POWER_Level_3,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_P3,
    },
    ACStatus.HEATING_LEVEL_4: {
        "power": config.AIR_CONDITIONER_POWER_Level_4,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_P4,
    },
    ACStatus.HEATING_LEVEL_5: {
        "power": config.AIR_CONDITIONER_POWER_Level_5,
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_P5,
    },
}

# Device configuration mapping
DEVICE_CONFIG = {
    "Television": {
        "power_rating": config.TELEVISION_POWER,
        "heating_rate": config.TELEVISION_HEATING_RATE
    },
    "Lamp": {
        "power_rating": config.LAMP_POWER,
        "heating_rate": config.LAMP_HEATING_RATE
    },
    "Bedside Lamp": {
        "power_rating": config.BEDSIDE_LAMP_POWER,
        "heating_rate": config.BEDSIDE_LAMP_HEATING_RATE
    },
    "Refrigerator": {
        "power_rating": config.REFRIGERATOR_POWER,
        "heating_rate": config.REFRIGERATOR_HEATING_RATE
    },
    "Electric Kettle": {
        "power_rating": config.ELECTRIC_KETTLE_POWER,
        "heating_rate": config.ELECTRIC_KETTLE_HEATING_RATE
    },
    "Air Conditioner": {
        "power_rating": config.AIR_CONDITIONER_POWER_Level_1,  # Default power level
        "heating_rate": config.AIR_CONDITIONER_HEATING_RATE_Level_N1  # Default heating rate
    }
}