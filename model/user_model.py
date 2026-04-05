"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          user_model.py                                                   *
* Purpose:       Implements the UserModel class for user authentication,         *
*                registration, and access level management.                      *
* Description:   Manages user credentials stored in a JSON database, supports    *
*                authentication, addition of users, and access validation.       *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o *
*                ChatGPT provided insights on JSON file handling, user           *
*                authentication logic, and secure access management.             *
**********************************************************************************
"""

#********************************** IMPORT ***************************************
# Standard library imports
import json
import os

# Application-specific imports
from utils.enums import AccessLevel

#**************************** CLASS DEFINITION ************************************

class UserModel:

    """
    A class to manage user credentials, authentication, and registration.
    
    Responsibilities:
    - Load and save user data from a JSON file.
    - Authenticate users based on their username and password.
    - Add new users and validate access levels for registration.
    """
    
    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Description: Initializes the UserModel and sets up the default Master user.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I initialize a class in Python and set a default value
    #               for a dictionary stored in a file?"
    # ------------------------------------------------------------------------------
    def __init__(self):

        """Initialize the UserModel class."""
        
        # Path to the JSON database
        self.db_path = os.path.join("database", "users.json")
        self._users = self._load_users() # Protected variable
        
        # Set up a default admin user.
        self.add_user("1", "1", AccessLevel.Master)

    # ------------------------------------------------------------------------------
    # Function:    _load_users
    # Description: Loads user data from the JSON database file.
    # Input:       None
    # Output:      dict: User data loaded from the file.
    # GPT Prompt:  "How can I load JSON data from a file in Python and handle missing
    #               or invalid files gracefully?"
    # ------------------------------------------------------------------------------
    def _load_users(self):

        """Load users from the database file."""

        if not os.path.exists(self.db_path):
            return {}  

        # Try to load the users from the database file.
        try:
            with open(self.db_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    # ------------------------------------------------------------------------------
    # Function:    save_users
    # Description: Saves the current user data back to the JSON file.
    # Input:       None
    # Output:      None
    # GPT Prompt:  "How can I save a Python dictionary to a JSON file with indentation?"
    # ------------------------------------------------------------------------------
    def save_users(self):

        """Save the current users dictionary to the database file."""

        with open(self.db_path, "w") as file:
            json.dump(self._users, file, indent=4)

    # ------------------------------------------------------------------------------
    # Function:    authenticate
    # Description: Validates the provided username and password.
    # Input:       username (str), password (str)
    # Output:      tuple: (bool: success, str: message, int: access_level or None)
    # GPT Prompt:  "How can I implement user authentication in Python with clear
    #               error messages for invalid input?"
    # ------------------------------------------------------------------------------
    def authenticate(self, username, password):

        """Check if the username and password match."""

        if not username and not password:
            return False, "Please enter username and password!", None
        elif not username:
            return False, "Please enter username!", None
        elif not password:
            return False, "Please enter password!", None
        elif self._users.get(username) is None:
            return False, "Username does not exist!", None
        else:
            if self._users.get(username)["password"] == password:
                current_access_level = self._users.get(username)["access_level"]
                return True, "Username and password match!", current_access_level
            else:
                return False, "Password is wrong!", None

    # ------------------------------------------------------------------------------
    # Function:    add_user
    # Description: Adds a new user to the database if the username doesn't exist.
    # Input:       username (str), password (str), access_level (AccessLevel)
    # Output:      bool: True if added, False otherwise.
    # GPT Prompt:  "How can I check for duplicate keys in a Python dictionary and
    #               update it with new values?"
    # ------------------------------------------------------------------------------
    def add_user(self, username, password, access_level):

        """Add a new user to the database."""
        
        # Password cannot be empty!
        if len(password.strip()) == 0:
            raise ValueError("Password cannot be empty!")

        if username in self._users:
            return False  # User already exists
        self._users[username] = {"password": password, "access_level": access_level.value}
        self.save_users()
        return True

    # ------------------------------------------------------------------------------
    # Function:    check_access
    # Description: Validates if the operator has the correct access level to add a user.
    # Input:       username (str), password (str), registration_level (AccessLevel)
    # Output:      tuple: (bool: success, str: message)
    # GPT Prompt:  "How can I validate user input and compare numeric values in
    #               Python for access management?"
    # ------------------------------------------------------------------------------    
    def check_access(self, username, password, registration_level):

        """Verify if the operator has the correct access level to add a new user to the database."""

        is_user_exist, message, _ = self.authenticate(username, password)
        if is_user_exist:
            if self._users.get(username)["access_level"] > registration_level.value:
                return True, "New account can be added"
            else:
                return False, "The admin's access level must be higher than the resgitration level"
        else:
            return False, message

