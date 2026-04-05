"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          enums.py                                                        *
* Purpose:       Defines enumerations for access levels, room types, device      *
*                statuses, and air conditioner states used across the system.    *
* Description:   Contains structured enumerations to manage constants for        *
*                user access levels, tab types, room classifications, device     *
*                states (TwoStatus), and AC operation levels (ACStatus).         *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o.*
*                ChatGPT provided guidance on designing clean and modular        *
*                enumerations for scalable software systems.                     *
**********************************************************************************
"""

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