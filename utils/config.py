from utils.enums import ACStatus
from utils.enums import RoomType
import utils.config as config

LOGGIN_WINDOW_WIDTH = 300
LOGGIN_WINDOW_HEIGHT = 400
POPUP_WINDOW_WIDTH = 300
POPUP_WINDOW_HEIGHT = 400

TEXT_PADY = 10 
BUTTON_PADY = 5 

HEADER_FONT = "Arial"
HEADER_SIZE = 17

LABEL_FONT = "Arial"
LABEL_SIZE = 12
LABEL_PADX = 5
LABEL_PADY = 5


WELCOME_MESSAGE = "Welcome to Intelligent Room"

















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
