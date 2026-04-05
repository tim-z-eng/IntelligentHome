#********************************** IMPORT ***************************************

import json
import os
from utils.enums import AccessLevel

#**************************** FUNCTIONS DEFINITIONS*******************************

class UserModel:
    def __init__(self):
        """Initialize the UserModel class."""
        # Path to the JSON database
        self.db_path = os.path.join("database", "users.json")
        self._users = self._load_users() # Protected variable
        
        # Set up a default admin user.
        self.add_user("1", "1", AccessLevel.Master)

    def _load_users(self):
        """Load users from the database file.
        
        Returns:
        dictionary -- Contain users information
        """
        if not os.path.exists(self.db_path):
            return {}  

        # Try to load the users from the database file.
        try:
            with open(self.db_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_users(self):
        """Save the current users dictionary to the database file."""
        with open(self.db_path, "w") as file:
            json.dump(self._users, file, indent=4)

    def authenticate(self, username, password):
        """Check if the username and password match.
        
        Keyword arguments:
        username(str) -- The username of the user
        password(str) -- The password of the user
        
        Returns:
        bool -- True if the username and password match, otherwise False
        """
        if not username and not password:
            return False, "Please enter username and password!"
        elif not username:
            return False, "Please enter username!"
        elif not password:
            return False, "Please enter password!"
        elif self._users.get(username) is None:
            return False, "Username does not exist!"
        else:
            if self._users.get(username)["password"] == password:
                current_access_level = self._users.get(username)["access_level"]
                return True, "Username and password match!", current_access_level
            else:
                return False, "Password is wrong!", None

    def add_user(self, username, password, access_level):
        """Add a new user to the database.
        
        Keyword arguments:
        username(str) -- The username of the user
        password(str) -- The password of the user
        access_level(int) -- The access level(Master or Admin) of the new user.
        
        Returns:
        bool -- True if the user is added successfully, Flase if the user already exists 
        """
        if username in self._users:
            return False  # User already exists
        self._users[username] = {"password": password, "access_level": access_level.value}
        self.save_users()
        return True
    
    def check_access(self, username, password, registration_level):
        """Verify if the operator has the correct access level to add a new user to the database.
        
        Keyword arguments:
        username(str) -- The username of the user
        password(str) -- The password of the user
        registration_level(int) -- The access level of the new user.
        
        Returns:
        bool -- True if the user is added successfully, Flase if the user already exists 
        """
        is_user_exist, message, _ = self.authenticate(username, password)
        if is_user_exist:
            if self._users.get(username)["access_level"] > registration_level.value:
                return True, "New account can be added"
            else:
                return False, "The admin's access level must be higher than the resgitration level"
        else:
            return False, message