#********************************** IMPORT ***************************************
import tkinter as tk
import utils.config as config
from tkinter import ttk, messagebox
from controller.controller import MainController
from utils.enums import AccessLevel
from PIL import Image, ImageTk
from view.base_view import View
from view.main_view import MainView

class LoginView(View):
    """A subclass of LoginView."""
    def _setup_ui(self):
        """Set up the GUI elements."""
        
        # Citation:
        # Scope: Use of ttk-themed widgets and the grid layout manager to improve the GUI's appearance.
        # Tool Name: ChatGPT-4o
        # Sample Prompt: "How to optimize tkinter with grid, can you give me an example?Thanks!"
        
        # Set up the grid layout manager and make sure it can be stretchable
        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)
        
        # Create a main frame and implement the grid layout manager
        main_frame = ttk.Frame(self._window, padding="25 25 20 20")
        main_frame.grid(row=0, column=0, sticky="NSEW")
        
        # Make internal GUI changes as the window is dragged
        for i in range(6):
            main_frame.rowconfigure(i, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label=ttk.Label(main_frame, text="Welcome", font=(config.HEADER_FONT, config.HEADER_SIZE))
        title_label.grid(row=0, column=0, pady=config.TEXT_PADY, sticky="w")
        
        # Citation:
        # Scope: Insert images in the GUI.
        # Tool Name: ChatGPT-4o
        # Sample Prompt: "How can I insert images in the Tkinter GUI?Thanks!
        
        # Load and scale the image
        img_path = "images/UBC.png"  # Path
        img = Image.open(img_path)
        resized_img = img.resize((80, 100), Image.Resampling.LANCZOS)  # Scale the image
        self._image = ImageTk.PhotoImage(resized_img)

        # UBC logo
        image_label = ttk.Label(main_frame, image=self._image)
        image_label.grid(row=0, column=1, padx=20, pady=20, sticky="E")
        
        # Username input
        username_label = ttk.Label(main_frame, text="Username", font=(config.LABEL_FONT, config.LABEL_SIZE))
        username_label.grid(row=1, column=0, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)
        self.__username_entry = ttk.Entry(main_frame, width=20) # Private variable
        self.__username_entry.grid(row=1, column=1, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)

        # Password input
        password_label = ttk.Label(main_frame, text="Password", font=(config.LABEL_FONT, config.LABEL_SIZE))
        password_label.grid(row=2, column=0, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)
        self.__password_entry = ttk.Entry(main_frame, show="*") # Private variable
        self.__password_entry.grid(row=2, column=1, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)

        # Login Button
        login_button = ttk.Button(main_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=config.BUTTON_PADY, sticky="EW")
        
        # Add admin button
        add_admin_button = ttk.Button(main_frame, text="Add admin", command=lambda: self.add_user_or_admin(AccessLevel.Admin))
        add_admin_button.grid(row=4, column=0, columnspan=2, pady=config.BUTTON_PADY, sticky="EW")
        
        # Add user button
        add_user_button = ttk.Button(main_frame, text="Add User", command=lambda: self.add_user_or_admin(AccessLevel.User))
        add_user_button.grid(row=5, column=0, columnspan=2, pady=config.BUTTON_PADY, sticky="EW")

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
        

    # def add_user_or_admin(self, access_level):
    #     """Open the Add User window.
        
    #     Keyword arguments:
    #     access_level(int) -- The access level(Master or Admin) of the new user.
    #     """
        
    #     # Different title for different access levels
    #     if access_level is AccessLevel.Admin:
    #         title = "Add New Admin"
    #     else:
    #         title = "Add New User"

    #     add_user_view = AddUserOrAdminView(self._controller, title, config.POPUP_WINDOW_WIDTH, config.LOGGIN_WINDOW_HEIGHT, tk.Toplevel(), access_level)
    #     add_user_view.run()

    # def show_main_view(self, current_access_level):
    #     """Transition to the main application view."""
    #     main_controller = MainController()
    #     main_view = MainView(main_controller, "Main Window", 800, 600, tk.Tk(), current_access_level)
    #     main_view.run()


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
                config.POPUP_WINDOW_WIDTH, 
                config.LOGGIN_WINDOW_HEIGHT, 
                tk.Toplevel(), 
                access_level
            )
            add_user_view.run()
        except ValueError as e:
            messagebox.showerror("Error", f"Error in adding user/admin: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

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

class AddUserOrAdminView(View):
    """A subclass of View that adds a new user."""
    def __init__(self, controller, title, width, height, window_function, access_level):
        """Initialize the AddUserOrAdminView class.
        Keyword arguments:
        controller -- The controller that manages the interaction between the view and model
        title(str) -- The title of the login window 
        width(int) -- The width of the login window 
        height(int) -- The height of the login window 
        window_function -- The window function to create the login window
        access_level(int) -- The access level(Master or Admin) of the new user.
        """
        self._access_level = access_level # Protected variable
        super().__init__(controller, title, width, height, window_function)

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