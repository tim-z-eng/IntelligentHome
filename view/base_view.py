"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          base_view.py                                                    *
* Purpose:       Defines the base View class for a Tkinter-based GUI application.*
* Description:   This file contains the definition of the `View` class,          *
*                which serves as a base class for all GUI views in the project.  *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o *
**********************************************************************************
"""


#********************************** IMPORT ***************************************
# Standard library imports
import tkinter as tk
from tkinter import ttk

#********************************** CLASS DEFINITION *****************************

class View:

    """A base class for a Tkinter-based GUI application."""

    # ------------------------------------------------------------------------------
    # Function:   __init__
    # Arguments:   controller (object) - The controller managing interaction between view and model.
    #              title (str) - The title of the GUI window.
    #              width (int) - The width of the GUI window.
    #              height (int) - The height of the GUI window.
    #              window_function (object) - The Tkinter window function.
    # Returns:     None
    # Description: Initializes the View base class with controller, title, size, and window function.
    # GPT Prompt:  How to initialize a Tkinter GUI window with a custom title, width, and height?
    # ------------------------------------------------------------------------------    
    def __init__(self, controller, title, width, height, window_function):
        self._controller = controller # Protected variable
        self._title = title
        self._window = window_function
        self._window.title(title)
        self._window.geometry(f"{width}x{height}")

        self._setup_ui()

    # ------------------------------------------------------------------------------
    # Function:    run
    # Arguments:   None
    # Returns:     None
    # Description: Runs the Tkinter main loop for the application.
    # GPT Prompt:  How to start the Tkinter main event loop?
    # ------------------------------------------------------------------------------
    def run(self):
        """Run the main loop of the Tkinter application."""
        self._window.mainloop() # Protected variable

    # ------------------------------------------------------------------------------
    # Function:    _setup_ui
    # Arguments:   None
    # Returns:     None
    # Description: Sets up the user interface for the View. Must be
    #              overridden by subclasses to define specific UI layout.
    # GPT Prompt:  How to set up a grid layout in Tkinter with widgets?
    # ------------------------------------------------------------------------------
    def _setup_ui(self):
        raise NotImplementedError("Subclasses must implement the _setup_ui method.")