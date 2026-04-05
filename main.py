#********************************** IMPORT ***************************************

import tkinter as tk
import utils.config as config
from controller.controller import AuthController
from view.login_view import LoginView

#********************************************************************************

def startup():

    auth_controller = AuthController()
    login_view = LoginView(auth_controller, "Login - Intelligent Home Appliance Control System", config.LOGIN_WINDOW_WIDTH, config.LOGIN_WINDOW_HEIGHT, tk.Tk())
    login_view.run()

if __name__ == "__main__":
    
    # Call the startup function
    startup()