#********************************** IMPORT ***************************************
import tkinter as tk
import utils.config as config
from tkinter import ttk, messagebox
from controller.controller import MainController
from utils.enums import AccessLevel
from PIL import Image, ImageTk

class View:
    """A base class for a Tkinter-based GUI application."""
    def __init__(self, controller, title, width, height, window_function):
        """Define a View base class for a Tkinter-based GUI application.
        Keyword arguments:
        controller -- The controller that manages the interaction between the view and model
        title(str) -- The title of the login window 
        width(int) -- The width of the login window 
        height(int) -- The height of the login window 
        window_function -- The window function to create the login window
        """
        self._controller = controller # Protected variable
        self._title = title
        self._window = window_function
        self._window.title(title)
        self._window.geometry(f"{width}x{height}")

        self._setup_ui()

    def run(self):
        """Run the main loop of the Tkinter application."""
        self._window.mainloop() # Protected variable