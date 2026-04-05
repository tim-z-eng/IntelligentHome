import tkinter as tk
import utils.config as config

from controller.controller import AuthController
from controller.controller import MainController
from view.login_view import LoginView
from view.main_view import MainView


def startup():
    # IMPORTANT: comment the follow before testing
    # auth_controller = AuthController()
    # login_view = LoginView(auth_controller, "Login - Intelligent Home Appliance Control System", config.LOGGIN_WINDOW_WIDTH, config.LOGGIN_WINDOW_HEIGHT, tk.Tk())
    # login_view.run()

    # # IMPORTANT: uncomment the follow before testing to disable the login process
    # This is only for test purpose, delete this before publishing
    main_controller = MainController()
    main_view = MainView(main_controller, "Main Window", 900, 900, tk.Tk(), 3)
    main_view.run()

if __name__ == "__main__":
    # Call the startup function
    startup()