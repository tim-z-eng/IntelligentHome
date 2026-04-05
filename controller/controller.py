#********************************** IMPORT ***************************************

from model.user_model import UserModel
from utils.enums import AccessLevel
from model.main_model import MainModel
from model.main_model import RoomTabModel
import model.electrical_device_model as elec_app
from utils.enums import TwoStatus as two_status

#********************************** IMPORT ***************************************

class AuthController:
    def __init__(self):
        """Initialize the AuthController class.
        
        Keyword arguments:
        user_model -- The model that manages the data information
        """
        self._user_model = UserModel() # Protected variable
        
    def login(self, username, password):
        """Handle user login.
        
        Keyword arguments:
        username(str) -- The username of the user
        password(str) -- The password of the user
        
        Returns:
        bool -- True if the user is authenticated, otherwise False         
        """
        can_loggin, message, current_access_level = self._user_model.authenticate(username, password)
        if can_loggin:
            return True, message, current_access_level
        raise ValueError(message)

    def check_access(self, username, password, registration_level):
        """Check if the user has the right access level to register a new user.
        
        Keyword arguments:
        username(str) -- The username of the user
        password(str) -- The password of the user
        registration_level(int) -- The registration level of the new user
        
        Returns:
        bool -- True if the user has the access level to register a new user, otherwise False
        """
        is_access, check_access_message = self._user_model.check_access(username,password, registration_level)
        if is_access:
            return True, "Register successfully"
        else:
            raise ValueError("Username does not exist")

    def register(self, username, password, registration_level):
        """Handle user registration.
        
        Keyword arguments:
        username(str) -- The username of the user
        password(str) -- The password of the user
        registration_level(int) -- The registration level of the new user
        
        Returns:
        bool -- True if the user is registered successfully, otherwise False
        """
        if self._user_model.add_user(username, password, registration_level):
            if registration_level == AccessLevel.Admin:
                return True, "Admin registered successfully"
            else:
                return True, "User registered successfully"
        raise ValueError("User already exists")

class MainController:
    def __init__(self):
        """Initialize the MainController class."""
        self.main_model = MainModel() # Protected variable
        self.view = None

    def initialize_tabs_in_view(self, view):
        """Initialize tabs in the view."""
        self.view = view

        # Iterate over tabs and check the tab_type
        for tab_full_name in self.main_model.get_tab_full_names():
                # Add Welcome tab
                self.view.add_tab_button(tab_full_name)
        self.show_tab_content("Welcome")

    def add_tab_button(self, tab_type):
        """Add a new tab and display its content."""
        if not tab_type:
            raise ValueError("Tab type must not be empty.")
        new_tab = self.main_model.add_tab(tab_type)
        tab_full_name = new_tab.tab_full_name
        self.view.add_tab_button(tab_full_name)
        self.show_tab_content(tab_full_name)
    
    # def show_tab_content(self, tab_full_name):
    #     devices_info = "None"
    #     _, room_temperature, devices_info = self.main_model.get_tab_info(tab_full_name)
    #     self.view.show_tab_content(tab_full_name, room_temperature, devices_info)

    def show_tab_content(self, tab_full_name):
        """Display the content of the specified tab."""
        if not tab_full_name:
            raise ValueError("Tab name must not be empty.")
        try:
            _, room_temperature, devices_info = self.main_model.get_tab_info(tab_full_name)
            self.view.show_tab_content(tab_full_name, room_temperature, devices_info)
        except ValueError as e:
            raise ValueError(f"Error retrieving tab content: {e}")

    def add_device(self, tab_to_be_added_on_name, device_type):

        tab_full_names = self.main_model.get_tab_full_names()

        for tab_full_name in tab_full_names:
            if tab_full_name == tab_to_be_added_on_name:
                try:
                    
                    self.main_model.add_device(tab_to_be_added_on_name, device_type)
                    self.main_model.save_tabs()
                    
                    self.show_tab_content(tab_to_be_added_on_name)
                    return True, None
                
                except ValueError as e:
                    raise ValueError(str(e))

        raise ValueError(f"Room {tab_to_be_added_on_name} not found.")
    
    def remove_current_device(self, tab_full_name, device_full_name):
        try:
            self.main_model.remove_current_device(tab_full_name, device_full_name)
            self.main_model.save_tabs()

            self.show_tab_content(tab_full_name)
            return True, None
        except ValueError as e:
            raise ValueError(str(e))
    
    # def change_device_state(self, tab_full_name, device_full_name, direction):
    #     """Change the state of the device."""
    #     self.main_model.change_device_state(tab_full_name, device_full_name, direction)
    #     self.main_model.save_tabs()

    #     self.show_tab_content(tab_full_name)

    def change_device_state(self, tab_full_name, device_full_name, direction):
        """Change the state of a device."""
        if not tab_full_name or not device_full_name or not direction:
            raise ValueError("Tab name, device name, and direction must not be empty.")
        if direction not in ["UP", "DOWN"]:
            raise ValueError(f"Invalid direction: {direction}")
        try:
            self.main_model.change_device_state(tab_full_name, device_full_name, direction)
            self.main_model.save_tabs()
            self.show_tab_content(tab_full_name)
        except ValueError as e:
            raise ValueError(f"Error changing device state: {e}")    