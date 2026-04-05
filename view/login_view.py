"""
**********************************************************************************
* Project:       IntelligentHome                                                 *
*                                                                                *
* Names:         Tianding Zhang, Yanlin Chen                                     *
* File:          login_view.py                                                   *
* Purpose:       Implements the LoginView and AddUserOrAdminView classes for the *
*                IntelligentHome project.                                        *
* Description:   Contains the definition of LoginView, a GUI for login and user  *
*                management functionalities, and AddUserOrAdminView, a GUI for   *
*                adding new users or administrators.                             *
*                                                                                *
* Citation:      This project was inspired and partially supported by ChatGPT 4o *
*                ChatGPT provided insights on Tkinter GUI design, layout         *
*                optimization, error handling, and comments in Python.           *
**********************************************************************************
"""

#********************************** IMPORT ***************************************
# Standard library imports
import tkinter as tk
from tkinter import ttk, messagebox

# Third-party imports
from PIL import Image, ImageTk

# Application-specific imports
import utils.config as config
from controller.controller import MainController
from utils.enums import AccessLevel
from view.base_view import View
from view.main_view import MainView

#********************************** CLASS DEFINITION *****************************

class LoginView(View):

    """
    A subclass of View to implement the login functionality.
    
    Responsibilities:
    - Handles user login by validating credentials and transitioning to the main application view.
    - Provides buttons to add users or administrators.
    """

    # ------------------------------------------------------------------------------
    # Function:    _setup_ui
    # Arguments:   None
    # Returns:     None
    # Description: Sets up the graphical user interface for the login view.
    # GPT Prompt:  "How can I create a login screen using Tkinter with labeled fields
    #               and a grid layout?"
    # ------------------------------------------------------------------------------
    def _setup_ui(self):

        """Set up the GUI elements."""

        # Set up the grid layout manager and make sure it can be stretchable
        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)
        
        # Create a main frame and implement the grid layout manager
        main_frame = ttk.Frame(self._window, padding=config.LOGIN_WINDOW_MAIN_FRAME_PAD)
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        # Make internal GUI changes as the window is dragged
        for i in range(6):
            main_frame.rowconfigure(i, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label=ttk.Label(main_frame, text="Welcome", font=(config.LOGIN_TITLE_FONT, config.LOGIN_TITLE_SIZE))
        title_label.grid(row=0, column=0, pady=config.LOGIN_TITLE_PADY, sticky="w")
        
        # Load and scale the image
        img_path = "images/UBC.png"  # Path
        img = Image.open(img_path)
        resized_img = img.resize((config.LOGIN_LOGO_WIDTH, config.LOGIN_LOGO_HEIGHT), Image.Resampling.LANCZOS)  # Scale the image
        self._image = ImageTk.PhotoImage(resized_img)

        # UBC logo
        image_label = ttk.Label(main_frame, image=self._image)
        image_label.grid(row=0, column=1, padx=config.LOGIN_LOGO_PADX, pady=config.LOGIN_LOGO_PADY, sticky="E")
        
        # Username input
        username_label = ttk.Label(main_frame, text=config.LOGIN_USERNAME_LABEL_TEXT, font=(config.LOGIN_USERNAME_LABEL_FONT, config.LOGIN_USERNAME_LABEL_SIZE))
        username_label.grid(row=1, column=0, sticky="NSEW", padx=config.LOGIN_USERNAME_LABEL_PADX, pady=config.LOGIN_USERNAME_LABEL_PADY)
        self.__username_entry = ttk.Entry(main_frame, width=config.LOGIN_USERNAME_ENTRY_WIDTH) # Private variable
        self.__username_entry.grid(row=1, column=1, sticky="NSEW", padx=config.LOGIN_USERNAME_ENTRY_PADX, pady=config.LOGIN_USERNAME_ENTRY_PADY)

        # Password input
        password_label = ttk.Label(main_frame, text=config.LOGIN_PASSWORD_LABEL_TEXT, font=(config.LOGIN_PASSWORD_LABEL_FONT, config.LOGIN_PASSWORD_LABEL_SIZE))
        password_label.grid(row=2, column=0, sticky="NSEW", padx=config.LOGIN_PASSWORD_LABEL_PADX, pady=config.LOGIN_PASSWORD_LABEL_PADY)
        self.__password_entry = ttk.Entry(main_frame, show="*") # Private variable
        self.__password_entry.grid(row=2, column=1, sticky="NSEW", padx=config.LOGIN_PASSWORD_ENTRY_PADX, pady=config.LOGIN_PASSWORD_ENTRY_PADY)

        # Login Button
        login_button = ttk.Button(main_frame, text=config.LOGIN_BUTTON_TEXT, command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=config.LOGIN_BUTTON_PADY, sticky="EW")
        
        # Add admin button
        add_admin_button = ttk.Button(main_frame, text=config.LOGIN_ADD_ADMIN_BUTTON_TEXT, command=lambda: self.add_user_or_admin(AccessLevel.Admin))
        add_admin_button.grid(row=4, column=0, columnspan=2, pady=config.LOGIN_ADD_ADMIN_BUTTON_PADY, sticky="EW")
        
        # Add user button
        add_user_button = ttk.Button(main_frame, text=config.LOGIN_ADD_USER_BUTTON_TEXT, command=lambda: self.add_user_or_admin(AccessLevel.User))
        add_user_button.grid(row=5, column=0, columnspan=2, pady=config.LOGIN_ADD_USER_BUTTON_PADY, sticky="EW")

    # ------------------------------------------------------------------------------
    # Function:    login
    # Arguments:   None
    # Returns:     None
    # Description: Handles login functionality by validating credentials and
    #              transitioning to the main application view if successful.
    # GPT Prompt:  "How can I validate user input in Tkinter and handle login?"
    # ------------------------------------------------------------------------------
    def login(self):

        """Handle login action."""

        try:
            
            # Get the username and password entered by the user on the login screen.
            username = self.__username_entry.get() # Private variable
            password = self.__password_entry.get()
            
            # Check if the username is a number
            if not username.isdigit():
                raise ValueError("Username can only contain numbers!")
            
            # Authenticate the user
            success, message, current_access_level = self._controller.login(username, password)
            if success:
                messagebox.showinfo("Login", message)
                self._window.destroy()  # Close the login window on success

                # Transition to MainView
                self.show_main_view(current_access_level)
            else:
                messagebox.showerror("Login", message)
        except ValueError as e:
            messagebox.showerror("Login", str(e))

    # ------------------------------------------------------------------------------
    # Function:    add_user_or_admin
    # Arguments:   access_level (AccessLevel) - The access level for the new user.
    # Returns:     None
    # Description: Opens a window to add a new user or administrator.
    # GPT Prompt:  "How can I dynamically create a new Tkinter window for user input?"
    # ------------------------------------------------------------------------------
    def add_user_or_admin(self, access_level):

        """Open the Add User window with enhanced validation and error handling."""

        try:
            # Validate access_level
            if access_level not in AccessLevel:
                raise ValueError(f"Invalid access level: {access_level}")
        
            # Different title for different access levels
            title = "Add New Admin" if access_level is AccessLevel.Admin else "Add New User"

            add_user_view = AddUserOrAdminView(
                self._controller, 
                title,
                config.REGISTER_WINDOW_WIDTH, 
                config.REGISTER_WINDOW_HEIGHT, 
                tk.Toplevel(), 
                access_level
            )
            add_user_view.run()
        except ValueError as e:
            messagebox.showerror("Error", f"Error in adding user/admin: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    # ------------------------------------------------------------------------------
    # Function:    show_main_view
    # Arguments:   current_access_level (AccessLevel) - The access level of the logged-in user.
    # Returns:     None
    # Description: Transitions to the main application view after successful login.
    # GPT Prompt:  "How can I switch from one Tkinter window to another while passing data?"
    # ------------------------------------------------------------------------------
    def show_main_view(self, current_access_level):

        """Transition to the main application view with enhanced validation and error handling."""

        try:
            # Validate current_access_level
            if current_access_level not in AccessLevel:
                raise ValueError(f"Invalid access level: {current_access_level}")

            main_controller = MainController()
            main_view = MainView(
                main_controller, 
                "Main Window", 
                800, 
                600, 
                tk.Tk(), 
                current_access_level
            )
            main_view.run()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid access level: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error occurred: {e}")

#********************************** CLASS DEFINITION *****************************

class AddUserOrAdminView(View):

    """
    A subclass of View that adds a new user or administrator.
    
    Responsibilities:
    - Handles user input for creating new user or admin accounts.
    - Validates inputs and interacts with the controller for user registration.
    """

    # ------------------------------------------------------------------------------
    # Function:    __init__
    # Arguments:   controller (object) - The controller managing interaction between view and model.
    #              title (str) - The title of the GUI window.
    #              width (int) - The width of the GUI window.
    #              height (int) - The height of the GUI window.
    #              window_function (object) - The Tkinter window function.
    #              access_level (AccessLevel) - The access level for the new user (Admin/User).
    # Returns:     None
    # Description: Initializes the AddUserOrAdminView class with controller, title,
    #              size, and window function.
    # GPT Prompt:  "How to create a GUI in Tkinter for user registration with validation?"
    # ------------------------------------------------------------------------------
    def __init__(self, controller, title, width, height, window_function, access_level):

        """Initialize the AddUserOrAdminView class."""

        self._access_level = access_level # Protected variable
        super().__init__(controller, title, width, height, window_function)

    # ------------------------------------------------------------------------------
    # Function:    _setup_ui
    # Arguments:   None
    # Returns:     None
    # Description: Sets up the graphical user interface for the add user/admin view.
    # GPT Prompt:  "How to create a form layout in Tkinter for user input fields?"
    # ------------------------------------------------------------------------------
    def _setup_ui(self):
        
        """Set up the GUI elements for adding a new user."""
        
        # Different words for different access levels
        if self._access_level is AccessLevel.Admin:
            supervisor_words = "Master Password"
            register_words = "Register As Admin"
            username_words = "New Adminname"
        else:
            supervisor_words = "Mater/Admin Username"
            register_words = "Register As User"
            username_words = "New Username"
            
        # Set up the grid layout manager and make sure it can be stretchable
        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)
        
        # Create a main frame and implement the grid layout manager
        main_frame = ttk.Frame(self._window, padding="25 25 20 20")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        # Make internal GUI changes as the window is dragged
        for i in range(10):
            main_frame.rowconfigure(i, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text=self._title, font=(config.HEADER_FONT, config.HEADER_SIZE))
        title_label.grid(row=0, column=0, columnspan=2, pady=config.TEXT_PADY)

        # Master/Admin username
        supervisor_label = ttk.Label(main_frame, text=supervisor_words, font=(config.LABEL_FONT, config.LABEL_SIZE))
        supervisor_label.grid(row=1, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
        self.__admin_username_entry = ttk.Entry(main_frame)
        self.__admin_username_entry.grid(row=2, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

        # Master/Admin password
        supervisor_pw_label = ttk.Label(main_frame, text=supervisor_words, font=(config.LABEL_FONT, config.LABEL_SIZE))
        supervisor_pw_label.grid(row=3, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
        self.__admin_password_entry = ttk.Entry(main_frame, show="*")
        self.__admin_password_entry.grid(row=4, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

        # New username
        new_username_label = ttk.Label(main_frame, text=username_words, font=(config.LABEL_FONT, config.LABEL_SIZE))
        new_username_label.grid(row=5, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
        self.__new_username_entry = ttk.Entry(main_frame)
        self.__new_username_entry.grid(row=6, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

        # New password
        new_password_label = ttk.Label(main_frame, text="New Password", font=(config.LABEL_FONT, config.LABEL_SIZE))
        new_password_label.grid(row=7, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
        self.__new_password_entry = ttk.Entry(main_frame, show="*")
        self.__new_password_entry.grid(row=8, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

        # Register button
        register_button = ttk.Button(main_frame, text=register_words, command=self.register_as_user_or_admin)
        register_button.grid(row=9, column=0, pady=config.BUTTON_PADY)

    # ------------------------------------------------------------------------------
    # Function:    register_as_user_or_admin
    # Arguments:   None
    # Returns:     None
    # Description: Handles the registration action by validating inputs and interacting
    #              with the controller to add a new user or admin.
    # GPT Prompt:  "How to validate user input in Tkinter and handle errors gracefully?"
    # ------------------------------------------------------------------------------
    def register_as_user_or_admin(self):

        """Handle registration action."""

        try:
            # Get the username and password entered by the user on the login screen.
            admin_username = self.__admin_username_entry.get()
            admin_password = self.__admin_password_entry.get()
            new_username = self.__new_username_entry.get()
            new_password = self.__new_password_entry.get()

            # Check if the username is a number
            if not new_username.isdigit():
                raise ValueError("The new username can only contain numbers!")

            # Authenticate admin credentials
            auth_success, auth_message = self._controller.check_access(admin_username, admin_password, self._access_level)
            if not auth_success:
                messagebox.showerror("Register", auth_message)
                return

            # Register new user
            success, message = self._controller.register(new_username, new_password, self._access_level)
            if success:
                messagebox.showinfo("Register", message)
                self._window.destroy()  # Close the add user window on success
            else:
                messagebox.showerror("Register", message)
        except ValueError as e:
            messagebox.showerror("Register", str(e))