from enum import Enum

class AccessLevel(Enum):
    User = 1
    Admin = 2
    Master = 3

class TabType(Enum):
    WELCOME = 1
    ROOM = 2

class RoomType(Enum):
    KITCHEN = "Kitchen"
    LIVING_ROOM = "Living Room"
    BEDROOM = "Bedroom"

class TwoStatus(Enum):
    OFF = 0
    ON = 1

class ACStatus(Enum):
    AC_MIN_LEVEL = -5
    COOLING_LEVEL_5 = -5
    COOLING_LEVEL_4 = -4
    COOLING_LEVEL_3 = -3
    COOLING_LEVEL_2 = -2
    COOLING_LEVEL_1 = -1
    OFF = 0
    AC_START = 0
    HEATING_LEVEL_1 = 1
    HEATING_LEVEL_2 = 2
    HEATING_LEVEL_3 = 3
    HEATING_LEVEL_4 = 4
    HEATING_LEVEL_5 = 5
    AC_MAX_LEVEL = 5