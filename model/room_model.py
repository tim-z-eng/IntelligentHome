import threading
import time
from utils.enums import RoomType
from utils.config import VALID_DEVICES, MAX_QUANTITY
import model.electrical_device_model as elec_app
from utils import config as config
from utils.enums import TwoStatus as two_status


class Room:
    def __init__(self, room_type, room_id):
        self.type = room_type
        self.id = room_id
        self.devices = []
        self.total_heat_rate = self.update_total_heat_rate()
        self.center_ac_states = {"TURN_OFF": 1, "COOLING": 2, "HEATING": 3}
        self.current_ac_state = "TURN_OFF"  # Start at TURN_OFF
        self.temperature = 25.0  # Initial temperature
        
        # This is a function table for center Air Conditioner finite state machine
        self.center_ac_states_transitions = {
            "TURN_OFF": lambda temp: "TURN_OFF" if 20 <= temp < 30 else "COOLING" if temp >= 30 else "HEATING",
            "COOLING": lambda temp: "TURN_OFF" if 20 <= temp < 25 else "COOLING" if temp >= 25 else "HEATING",
            "HEATING": lambda temp: "TURN_OFF" if 25 <= temp < 30 else "COOLING" if 30 <= temp else "HEATING",
        }

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self.update_room_temperature, daemon=True)
        self._thread.start()

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
            print(f"device_to_remove")
            # Remove the device
            self.devices.remove(device_with_largest_id)
            self.update_total_heat_rate()
            return

        except ValueError as e:
            raise ValueError(f"Failed to remove device: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while removing the device: {str(e)}")
    
    def get_devices_info(self):
        devices_info = []
        for device in self.devices:
            device_info = (device.device_full_name, device.status)
            devices_info.append(device_info)
        return devices_info
    
    def get_room_temperature(self):
        return self.temperature
    
    def change_device_state(self, device_full_name, direction):

        for device in self.devices:
            if device.device_full_name == device_full_name:
                if direction == "UP":
                    device.switch_up()
                else:
                    device.switch_down()
        self.update_total_heat_rate()
        

    def update_total_heat_rate(self):
        total_heat_rate = 0
        for device in self.devices:
            total_heat_rate += device.heating_rate
        self.total_heat_rate = total_heat_rate
        return total_heat_rate

    def update_room_temperature(self):
        while not self._stop_event.is_set():
            self.current_ac_state = self.center_ac_states_transitions[self.current_ac_state](self.temperature)
            print(f"{self.total_heat_rate}")
            if self.current_ac_state == "TURN_OFF":
                self.temperature += 0.001 * self.total_heat_rate * 1.0
                print("TURN_OFF")
            elif self.current_ac_state == "COOLING":
                self.temperature -= 0.3
                print("COOLING")
            elif self.current_ac_state == "HEATING":
                self.temperature += 0.3
                print("HEATING")
            else:
                raise ValueError(f"Center AC state: {self.current_ac_state} is not defined")
            time.sleep(1.0)

    def stop_thread(self):
        try:
            self._stop_event.set()
            self._thread.join()
            return
        except ValueError as e:
            raise ValueError(str(e))

class Kitchen(Room):
    def __init__(self, room_id):
        super().__init__(room_type=RoomType.KITCHEN.value, room_id=room_id)
        self.valid_devices = VALID_DEVICES[RoomType.KITCHEN]
        self.max_quantity = MAX_QUANTITY[RoomType.KITCHEN]

class LivingRoom(Room):
    def __init__(self, room_id):
        super().__init__(room_type=RoomType.LIVING_ROOM.value, room_id=room_id)
        self.valid_devices = VALID_DEVICES[RoomType.LIVING_ROOM]
        self.max_quantity = MAX_QUANTITY[RoomType.LIVING_ROOM]

class Bedroom(Room):
    def __init__(self, room_id):
        super().__init__(room_type=RoomType.BEDROOM.value, room_id=room_id)
        self.valid_devices = VALID_DEVICES[RoomType.BEDROOM]
        self.max_quantity = MAX_QUANTITY[RoomType.BEDROOM]