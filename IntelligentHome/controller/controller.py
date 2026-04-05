from model.user_model import UserModel
from utils.enums import AccessLevel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self, username, password):
        """Handle user login."""
        can_loggin, message = self.user_model.authenticate(username, password)
        if can_loggin:
            return True, message
        return False, message
    
    def check_access(self, username, password, registration_level):
        is_access, check_access_message = self.user_model.check_access(username,password, registration_level)
        if is_access:
            return True, "Can be register successfully"
        else:
            return False, check_access_message

    def register(self, username, password, registration_level):
        """Handle user registration."""
        if self.user_model.add_user(username, password, registration_level):
            return True, "User registered successfully"
        return False, "User already exists"

# class MainController:
#     def _init_(self):
#         self.main_model = MainModel()