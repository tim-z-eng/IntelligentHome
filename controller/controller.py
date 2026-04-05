"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          controller.py                                                   *
* Purpose:       Implements AuthController and MainController classes for the    *
*                IntelligentHome project.                                        *
* Description:   AuthController manages user authentication and registration,    *
*                while MainController handles room and device operations, such   *
*                as adding rooms, managing devices, and updating tab contents.   *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o *
*                ChatGPT provided insights on class design, error handling,      *
*                dynamic room/device management and comments in Python.          *
**********************************************************************************
"""

#********************************** IMPORT ***************************************
from model.user_model import UserModel
from utils.enums import AccessLevel
from model.main_model import MainModel

#********************************** CLASS DEFINITION *****************************

class AuthController:

    """
    A controller class to manage user authentication and registration processes.
    
    Responsibilities:
    - Handles login functionality.
    - Checks access levels for user registration.
    - Manages user and admin registration processes.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Arguments:   None
    # Returns:     None
    # Description: Initializes the AuthController class and sets up the UserModel.
    # GPT PROMPT:  "How do I design a controller class to handle user authentication 
    #              and integrate it with a user model in Python?"
    # ------------------------------------------------------------------------------    
    def __init__(self):

        """Initialize the AuthController class."""

        self._user_model = UserModel() # Protected variable

    # ------------------------------------------------------------------------------
    # Function:    login
    # Arguments:   username (str) - Username for login.
    #              password (str) - Password for login.
    # Returns:     tuple - (bool, str, AccessLevel) indicating success and user access level.
    # Description: Handles user login and validates credentials.
    # GPT PROMPT:  "How do I validate user credentials in Python and return specific 
    #              messages based on success or failure?"
    # ------------------------------------------------------------------------------        
    def login(self, username, password):

        """Handle user login."""

        can_loggin, message, current_access_level = self._user_model.authenticate(username, password)
        if can_loggin:
            return True, message, current_access_level
        raise ValueError(message)

    # ------------------------------------------------------------------------------
    # Function:    check_access
    # Arguments:   username (str) - Username for validation.
    #              password (str) - Password for validation.
    #              registration_level (int) - Level of access to register new users.
    # Returns:     tuple - (bool, str) confirming access or failure.
    # Description: Verifies if a user has the necessary access level to register new users.
    # GPT PROMPT:  "How can I check user access levels before allowing a specific operation 
    #              in Python, and raise appropriate errors if invalid?"
    # ------------------------------------------------------------------------------
    def check_access(self, username, password, registration_level):

        """Check if the user has the right access level to register a new user."""

        is_access, check_access_message = self._user_model.check_access(username,password, registration_level)
        if is_access:
            return True, "Register successfully"
        else:
            raise ValueError("Username does not exist")

    # ------------------------------------------------------------------------------
    # Function:    register
    # Arguments:   username (str) - Username for the new account.
    #              password (str) - Password for the new account.
    #              registration_level (int) - Access level for the new user.
    # Returns:     tuple - (bool, str) confirming successful registration.
    # Description: Handles user and admin registration processes.
    # GPT PROMPT:  "How do I design a method to add users with specific access levels, 
    #              ensuring duplicates are not allowed?"
    # ------------------------------------------------------------------------------
    def register(self, username, password, registration_level):

        """Handle user registration."""

        if self._user_model.add_user(username, password, registration_level):
            if registration_level == AccessLevel.Admin:
                return True, "Admin registered successfully"
            else:
                return True, "User registered successfully"
        raise ValueError("User already exists")
    
#********************************** CLASS DEFINITION *****************************

class MainController:

    """
    A controller class to manage room and device operations.
    
    Responsibilities:
    - Initializes tabs for the main view.
    - Manages adding rooms, devices, and updating room/device content dynamically.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Arguments:   None
    # Returns:     None
    # Description: Initializes the MainController class and sets up the MainModel.
    # GPT PROMPT:  "How can I structure a controller class to manage dynamic views 
    #              and interact with the model layer efficiently?"
    # ------------------------------------------------------------------------------   
    def __init__(self):

        """Initialize the MainController class."""

        self.main_model = MainModel() # Protected variable
        self.view = None

    # ------------------------------------------------------------------------------
    # Function:    initialize_tabs_in_view
    # Arguments:   view (object) - The main view to initialize tabs.
    # Returns:     None
    # Description: Adds existing tabs to the main view and sets up the Welcome tab.
    # GPT PROMPT:  "How do I initialize dynamic tabs in a Python GUI application?"
    # ------------------------------------------------------------------------------
    def initialize_tabs_in_view(self, view):

        """Initialize tabs in the view."""

        self.view = view

        # Iterate over tabs and check the tab_type
        for tab_full_name in self.main_model.get_tab_full_names():
                # Add Welcome tab
                self.view.add_tab_button(tab_full_name)
        self.show_tab_content("Welcome")

    # ------------------------------------------------------------------------------
    # Function:    add_tab_button
    # Arguments:   tab_type (str) - Type/name of the tab to add.
    # Returns:     None
    # Description: Adds a new tab to the main view and displays its content.
    # GPT PROMPT:  "How can I dynamically add tabs to a Tkinter GUI while updating the view?"
    # ------------------------------------------------------------------------------
    def add_tab_button(self, tab_type):

        """Add a new tab and display its content."""

        if not tab_type:
            raise ValueError("Tab type must not be empty.")
        new_tab = self.main_model.add_tab(tab_type)
        tab_full_name = new_tab.tab_full_name
        self.view.add_tab_button(tab_full_name)
        self.show_tab_content(tab_full_name)

    # ------------------------------------------------------------------------------
    # Function:    show_tab_content
    # Arguments:   tab_full_name (str) - The name of the tab to display.
    # Returns:     None
    # Description: Retrieves and displays the content for the specified tab.
    # GPT PROMPT:  "How do I fetch and display data dynamically in a specific section 
    #              of a Tkinter GUI?"
    # ------------------------------------------------------------------------------
    def show_tab_content(self, tab_full_name):

        """Display the content of the specified tab."""

        if not tab_full_name:
            raise ValueError("Tab name must not be empty.")
        try:
            _, room_temperature, devices_info = self.main_model.get_tab_info(tab_full_name)
            self.view.show_tab_content(tab_full_name, room_temperature, devices_info)
        except ValueError as e:
            raise ValueError(f"Error retrieving tab content: {e}")

    # ------------------------------------------------------------------------------
    # Function:    add_device
    # Arguments:   tab_to_be_added_on_name (str) - The name of the room to add the device to.
    #              device_type (str) - The type of device to add.
    # Returns:     tuple - (bool, None) confirming success.
    # Description: Adds a new device to the specified room.
    # GPT PROMPT:  "How can I dynamically add devices to a room and update the GUI in Python?"
    # ------------------------------------------------------------------------------
    def add_device(self, tab_to_be_added_on_name, device_type):

        """Add a new device to a specified tab (room)."""

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

    # ------------------------------------------------------------------------------
    # Function:    remove_current_device
    # Arguments:   tab_full_name (str) - The name of the room.
    #              device_full_name (str) - The name of the device to remove.
    # Returns:     tuple - (bool, None) confirming success.
    # Description: Removes the specified device from the room.
    # GPT PROMPT:  "How do I delete an item from a specific list in Python and update the view?"
    # ------------------------------------------------------------------------------    
    def remove_current_device(self, tab_full_name, device_full_name):

        """Remove a device from a specified tab (room)."""

        try:
            self.main_model.remove_current_device(tab_full_name, device_full_name)
            self.main_model.save_tabs()

            self.show_tab_content(tab_full_name)
            return True, None
        except ValueError as e:
            raise ValueError(str(e))

    # ------------------------------------------------------------------------------
    # Function:    change_device_state
    # Arguments:   tab_full_name (str) - The name of the room.
    #              device_full_name (str) - The name of the device.
    #              direction (str) - The new state ("UP" or "DOWN").
    # Returns:     None
    # Description: Changes the state of the specified device.
    # GPT PROMPT:  "How can I manage state changes for devices in Python and update the view?"
    # ------------------------------------------------------------------------------
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