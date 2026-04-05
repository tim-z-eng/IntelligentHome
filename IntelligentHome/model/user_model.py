import json
import os
from utils.enums import AccessLevel


class UserModel:
    def __init__(self):
        # Path to the JSON database
        self.db_path = os.path.join("database", "users.json")
        self.users = self.load_users()
        self.add_user("1", "1", AccessLevel.Master)

    def load_users(self):
        """Load users from the database file."""
        if not os.path.exists(self.db_path):
            return {}  # Return an empty dictionary if the file doesn't exist
        with open(self.db_path, "r") as file:
            return json.load(file)

    def save_users(self):
        """Save the current users dictionary to the database file."""
        with open(self.db_path, "w") as file:
            json.dump(self.users, file, indent=4)

    def authenticate(self, username, password):
        """Check if the username and password match."""
        if self.users.get(username) is None:
            return False, "Username does not exist"
        else:
            if self.users.get(username)["password"] == password:
                return True, "Username and password match"
            else:
                return False, "password is wrong"
    
    def check_access(self, username, password, registration_level):
        is_user_exist, message = self.authenticate(username, password)
        if is_user_exist:
            if self.users.get(username)["access_level"] > registration_level.value:
                return True, "New account can be added"
            else:
                return False, "The admin's access level must be higher than the resgitration level"
        else:
            return False, message

    def add_user(self, username, password, access_level):
        """Add a new user to the database."""
        if username in self.users:
            return False  # User already exists
        self.users[username] = {"password": password, "access_level": access_level.value}
        self.save_users()
        return True
