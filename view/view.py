# #********************************** IMPORT ***************************************
# import tkinter as tk
# import utils.config as config
# from tkinter import ttk, messagebox
# from controller.controller import MainController
# from utils.enums import AccessLevel
# from PIL import Image, ImageTk

# #********************************** IMPORT ***************************************

# class View:
#     """A base class for a Tkinter-based GUI application."""
#     def __init__(self, controller, title, width, height, window_function):
#         """Define a View base class for a Tkinter-based GUI application.
#         Keyword arguments:
#         controller -- The controller that manages the interaction between the view and model
#         title(str) -- The title of the login window 
#         width(int) -- The width of the login window 
#         height(int) -- The height of the login window 
#         window_function -- The window function to create the login window
#         """
#         self._controller = controller # Protected variable
#         self._title = title
#         self._window = window_function
#         self._window.title(title)
#         self._window.geometry(f"{width}x{height}")

#         self._setup_ui()

#     def _setup_ui(self):
#         """Set up the GUI elements."""
        
#         # This method should be overridden by derived classes.
#         raise NotImplementedError("this is a base class, don't call this")
        
#     def run(self):
#         """Run the main loop of the Tkinter application."""
#         self._window.mainloop() # Protected variable

# class LoginView(View):
#     """A subclass of LoginView."""
#     def _setup_ui(self):
#         """Set up the GUI elements."""
        
#         # Citation:
#         # Scope: Use of ttk-themed widgets and the grid layout manager to improve the GUI's appearance.
#         # Tool Name: ChatGPT-4o
#         # Sample Prompt: "How to optimize tkinter with grid, can you give me an example?Thanks!"
        
#         # Set up the grid layout manager and make sure it can be stretchable
#         self._window.rowconfigure(0, weight=1)
#         self._window.columnconfigure(0, weight=1)
        
#         # Create a main frame and implement the grid layout manager
#         main_frame = ttk.Frame(self._window, padding="25 25 20 20")
#         main_frame.grid(row=0, column=0, sticky="NSEW")
        
#         # Make internal GUI changes as the window is dragged
#         for i in range(6):
#             main_frame.rowconfigure(i, weight=1)
#         main_frame.columnconfigure(0, weight=1)
#         main_frame.columnconfigure(1, weight=1)
        
#         # Title
#         title_label=ttk.Label(main_frame, text="Welcome", font=(config.HEADER_FONT, config.HEADER_SIZE))
#         title_label.grid(row=0, column=0, pady=config.TEXT_PADY, sticky="w")
        
#         # Citation:
#         # Scope: Insert images in the GUI.
#         # Tool Name: ChatGPT-4o
#         # Sample Prompt: "How can I insert images in the Tkinter GUI?Thanks!
        
#         # Load and scale the image
#         img_path = "images/UBC.png"  # Path
#         img = Image.open(img_path)
#         resized_img = img.resize((80, 100), Image.Resampling.LANCZOS)  # Scale the image
#         self._image = ImageTk.PhotoImage(resized_img)

#         # UBC logo
#         image_label = ttk.Label(main_frame, image=self._image)
#         image_label.grid(row=0, column=1, padx=20, pady=20, sticky="E")
        
#         # Username input
#         username_label = ttk.Label(main_frame, text="Username", font=(config.LABEL_FONT, config.LABEL_SIZE))
#         username_label.grid(row=1, column=0, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)
#         self.__username_entry = ttk.Entry(main_frame, width=20) # Private variable
#         self.__username_entry.grid(row=1, column=1, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)

#         # Password input
#         password_label = ttk.Label(main_frame, text="Password", font=(config.LABEL_FONT, config.LABEL_SIZE))
#         password_label.grid(row=2, column=0, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)
#         self.__password_entry = ttk.Entry(main_frame, show="*") # Private variable
#         self.__password_entry.grid(row=2, column=1, sticky="NSEW", padx=config.LABEL_PADX, pady=config.LABEL_PADY)

#         # Login Button
#         login_button = ttk.Button(main_frame, text="Login", command=self.login)
#         login_button.grid(row=3, column=0, columnspan=2, pady=config.BUTTON_PADY, sticky="EW")
        
#         # Add admin button
#         add_admin_button = ttk.Button(main_frame, text="Add admin", command=lambda: self.add_user_or_admin(AccessLevel.Admin))
#         add_admin_button.grid(row=4, column=0, columnspan=2, pady=config.BUTTON_PADY, sticky="EW")
        
#         # Add user button
#         add_user_button = ttk.Button(main_frame, text="Add User", command=lambda: self.add_user_or_admin(AccessLevel.User))
#         add_user_button.grid(row=5, column=0, columnspan=2, pady=config.BUTTON_PADY, sticky="EW")

#     def login(self):
#         """Handle login action."""
#         try:
            
#             # Get the username and password entered by the user on the login screen.
#             username = self.__username_entry.get() # Private variable
#             password = self.__password_entry.get()
            
#             # Check if the username is a number
#             if not username.isdigit():
#                 raise ValueError("Username can only contain numbers!")
            
#             # Authenticate the user
#             success, message, current_access_level = self._controller.login(username, password)
#             if success:
#                 messagebox.showinfo("Login", message)
#                 self._window.destroy()  # Close the login window on success

#                 # Transition to MainView
#                 self.show_main_view(current_access_level)
#             else:
#                 messagebox.showerror("Login", message)
#         except ValueError as e:
#             messagebox.showerror("Login", str(e))        
        

#     def add_user_or_admin(self, access_level):
#         """Open the Add User window.
        
#         Keyword arguments:
#         access_level(int) -- The access level(Master or Admin) of the new user.
#         """
        
#         # Different title for different access levels
#         if access_level is AccessLevel.Admin:
#             title = "Add New Admin"
#         else:
#             title = "Add New User"

#         add_user_view = AddUserOrAdminView(self._controller, title, config.POPUP_WINDOW_WIDTH, config.LOGGIN_WINDOW_HEIGHT, tk.Toplevel(), access_level)
#         add_user_view.run()

#     def show_main_view(self, current_access_level):
#         """Transition to the main application view."""
#         main_controller = MainController()
#         main_view = MainView(main_controller, "Main Window", 800, 600, tk.Tk(), current_access_level)
#         main_view.run()

# class AddUserOrAdminView(View):
#     """A subclass of View that adds a new user."""
#     def __init__(self, controller, title, width, height, window_function, access_level):
#         """Initialize the AddUserOrAdminView class.
#         Keyword arguments:
#         controller -- The controller that manages the interaction between the view and model
#         title(str) -- The title of the login window 
#         width(int) -- The width of the login window 
#         height(int) -- The height of the login window 
#         window_function -- The window function to create the login window
#         access_level(int) -- The access level(Master or Admin) of the new user.
#         """
#         self._access_level = access_level # Protected variable
#         super().__init__(controller, title, width, height, window_function)

#     def _setup_ui(self):
#         """Set up the GUI elements for adding a new user."""
        
#         # Different words for different access levels
#         if self._access_level is AccessLevel.Admin:
#             supervisor_words = "Master Password"
#             register_words = "Register As Admin"
#             username_words = "New Adminname"
#         else:
#             supervisor_words = "Mater/Admin Username"
#             register_words = "Register As User"
#             username_words = "New Username"
            
#         # Set up the grid layout manager and make sure it can be stretchable
#         self._window.rowconfigure(0, weight=1)
#         self._window.columnconfigure(0, weight=1)
        
#         # Create a main frame and implement the grid layout manager
#         main_frame = ttk.Frame(self._window, padding="25 25 20 20")
#         main_frame.grid(row=0, column=0, sticky="NSEW")
        
#         # Make internal GUI changes as the window is dragged
#         for i in range(10):
#             main_frame.rowconfigure(i, weight=1)
#         main_frame.columnconfigure(0, weight=1)
        
#         # Title
#         title_label = ttk.Label(main_frame, text=self._title, font=(config.HEADER_FONT, config.HEADER_SIZE))
#         title_label.grid(row=0, column=0, columnspan=2, pady=config.TEXT_PADY)

#         # Master/Admin username
#         supervisor_label = ttk.Label(main_frame, text=supervisor_words, font=(config.LABEL_FONT, config.LABEL_SIZE))
#         supervisor_label.grid(row=1, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
#         self.__admin_username_entry = ttk.Entry(main_frame)
#         self.__admin_username_entry.grid(row=2, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

#         # Master/Admin password
#         supervisor_pw_label = ttk.Label(main_frame, text=supervisor_words, font=(config.LABEL_FONT, config.LABEL_SIZE))
#         supervisor_pw_label.grid(row=3, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
#         self.__admin_password_entry = ttk.Entry(main_frame, show="*")
#         self.__admin_password_entry.grid(row=4, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

#         # New username
#         new_username_label = ttk.Label(main_frame, text=username_words, font=(config.LABEL_FONT, config.LABEL_SIZE))
#         new_username_label.grid(row=5, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
#         self.__new_username_entry = ttk.Entry(main_frame)
#         self.__new_username_entry.grid(row=6, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

#         # New password
#         new_password_label = ttk.Label(main_frame, text="New Password", font=(config.LABEL_FONT, config.LABEL_SIZE))
#         new_password_label.grid(row=7, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)
#         self.__new_password_entry = ttk.Entry(main_frame, show="*")
#         self.__new_password_entry.grid(row=8, column=0, padx=config.LABEL_PADX, pady=config.LABEL_PADY)

#         # Register button
#         register_button = ttk.Button(main_frame, text=register_words, command=self.register_as_user_or_admin)
#         register_button.grid(row=9, column=0, pady=config.BUTTON_PADY)


#     def register_as_user_or_admin(self):
#         """Handle registration action."""
#         try:
#             # Get the username and password entered by the user on the login screen.
#             admin_username = self.__admin_username_entry.get()
#             admin_password = self.__admin_password_entry.get()
#             new_username = self.__new_username_entry.get()
#             new_password = self.__new_password_entry.get()

#             # Check if the username is a number
#             if not new_username.isdigit():
#                 raise ValueError("The new username can only contain numbers!")

#             # Authenticate admin credentials
#             auth_success, auth_message = self._controller.check_access(admin_username, admin_password, self._access_level)
#             if not auth_success:
#                 messagebox.showerror("Register", auth_message)
#                 return

#             # Register new user
#             success, message = self._controller.register(new_username, new_password, self._access_level)
#             if success:
#                 messagebox.showinfo("Register", message)
#                 self._window.destroy()  # Close the add user window on success
#             else:
#                 messagebox.showerror("Register", message)
#         except ValueError as e:
#             messagebox.showerror("Register", str(e))

# class MainView(View):
#     def __init__(self, controller, title, width, height, window_function, access_level):
#         """Initialize the AddUserOrAdminView class.
#         Keyword arguments:
#         controller -- The controller that manages the interaction between the view and model
#         title(str) -- The title of the login window 
#         width(int) -- The width of the login window 
#         height(int) -- The height of the login window 
#         window_function -- The window function to create the login window
#         access_level(int) -- The access level(Master or Admin) of the new user.
#         """
#         self._access_level = access_level # Protected variable
#         super().__init__(controller, title, width, height, window_function)
    
#     """A subclass of View that displays the main application window."""
#     def _setup_ui(self):
#         """Set up the GUI for the main application window."""
        
#          # Set up the grid layout manager and make sure it can be stretchable
#         self._window.rowconfigure(0, weight=1)
#         self._window.columnconfigure(0, weight=1)
        
#         # Create a main frame and implement the grid layout manager
#         self._main_frame = ttk.Frame(self._window, padding="5 5 5 5")
#         self._main_frame.grid(row=0, column=0, sticky="NSEW")
        
#         # Make internal GUI changes as the window is dragged
#         self._main_frame.rowconfigure(0, weight=1)
#         self._main_frame.columnconfigure(0, weight=0)
#         self._main_frame.columnconfigure(1, weight=1) 
        
#         # Create a frame for side tabs
#         self._tab_frame = ttk.Frame(self._main_frame)
#         self._tab_frame.grid(row=0, column=0, sticky="NS")
#         self._tab_frame.rowconfigure(0, weight=0)
#         self._tab_frame.columnconfigure(0, weight=1)
        
#         # Create a frame for tab content
#         self._content_frame = ttk.Frame(self._main_frame, style="TFrame")
#         self._content_frame.grid(row=0, column=1, sticky="NSEW")
#         self._content_frame.columnconfigure(0, weight=1)

#         if self._access_level >= AccessLevel.Master.value:
#             self._main_frame.rowconfigure(1, weight=0)
#             add_room_button = ttk.Button(self._main_frame, text="Add Room", command=self.add_room_or_device)
#             add_room_button.grid(row=1, column=0, columnspan=2, pady=config.BUTTON_PADY)

#         self._controller.initialize_tabs_in_view(self)
#         self.keep_refresh_tab_content()

#         self._current_tab_full_name = None  

#     def add_tab_button(self, tab_full_name):
        
#         # Citation:
#         # Scope: Newly added devices appear one after another
#         # Tool Name: ChatGPT-4o
#         # Sample Prompt: "How can I use grid to ensure newly added devices appear one after another?Thanks!"

#         # Counts the number of existing button
#         current_rows = len(self._tab_frame.grid_slaves())
#         tab_button = ttk.Button(self._tab_frame,text=tab_full_name,command=lambda: self._controller.show_tab_content(tab_full_name))
#         tab_button.grid(row=current_rows, column=0, pady=5)

    
#     def show_tab_content(self, tab_full_name, room_temperature, devices_info):
#         self._current_tab_full_name = tab_full_name
#         for widget in self._content_frame.winfo_children():
#             widget.destroy()

#         # Title
#         title_label = ttk.Label(self._content_frame, text=tab_full_name, font=("Arial", 20))
#         title_label.grid(row=0, column=0, pady=50, sticky="N")

#         # Show temperature
#         temp_text = f"Room Temperature: {room_temperature:.3f}" if room_temperature is not None else ""
#         temp_label = ttk.Label(self._content_frame, text=temp_text, font=("Arial", 15))
#         temp_label.grid(row=1, column=0, pady=50, sticky="N")

#         current_row = 2

#         # Check if "Welcome"
#         if tab_full_name != "Welcome":
#             devices_label = ttk.Label(self._content_frame, text="Devices:", font=("Arial", 15))
#             devices_label.grid(row=current_row, column=0, pady=10, sticky="N")
#             current_row += 1

#             if devices_info is not None:
#                 devices_frame = ttk.Frame(self._content_frame)
#                 devices_frame.grid(row=current_row, column=0, sticky="EW", padx=10, pady=5)
#                 devices_frame.columnconfigure(0, weight=1)

#                 device_row = 0
#                 for device_name, state in devices_info:
#                     device_frame = ttk.Frame(devices_frame, relief="solid")
#                     device_frame.grid(row=device_row, column=0, sticky="EW", pady=5, padx=10)

#                     device_frame.columnconfigure(0, weight=1)

#                     ttk.Label(device_frame, text=f"Device: {device_name}", font=("Arial", 12)).grid(row=0, column=0, padx=10, sticky="W")
#                     ttk.Label(device_frame, text=f"Status: {state}", font=("Arial", 12)).grid(row=0, column=1, padx=10, sticky="W")
                    
#                     style = ttk.Style()

#                     # Define the green button style
#                     style.configure("Green.TButton", background="green")
                    
#                     # Define the yellow button style
#                     style.configure("yellow.TButton", background="yellow")
                    
#                     # Define the red button style
#                     style.configure("Red.TButton",background="red")    

#                     switch_down_button=ttk.Button(
#                         device_frame, 
#                         text="Switch Down", 
#                         style="Green.TButton",
#                         command=lambda d=device_name: self._controller.change_device_state(tab_full_name, d, "DOWN")
#                     )
#                     switch_down_button.grid(row=0, column=2, padx=5)
                    
#                     if self._access_level >= AccessLevel.Admin.value:
#                         remove_device_button=ttk.Button(
#                             device_frame, 
#                             text="Remove", 
#                             style="yellow.TButton",
#                             command=lambda d=device_name: self._controller.remove_current_device(tab_full_name, d)
#                         )
#                         remove_device_button.grid(row=0, column=3, padx=5)
                    
#                     switch_up_button=ttk.Button(
#                         device_frame, 
#                         text="Switch Up", 
#                         style="Red.TButton",
#                         command=lambda d=device_name: self._controller.change_device_state(tab_full_name, d, "UP")
#                         )
#                     switch_up_button.grid(row=0, column=4, padx=5)

#                     device_row += 1

#                 current_row += 1

#             if self._access_level >= AccessLevel.Admin.value:
#                 # Add device button
#                 add_device_button = ttk.Button(
#                     self._content_frame,
#                     text="Add Device",
#                     command=lambda: self.add_room_or_device(tab_full_name)
#                 )
#                 add_device_button.grid(row=current_row, column=0, pady=20)
    
#     def add_room_or_device(self, tab_name=None):
#         """Open Add Room or Add Devide window."""
        
#         if tab_name is None:
#             title = "Add Room" # If tab_name is None, add a room
#         else:
#             title = f"Add Device to {tab_name}" # If tab_name is not None, add a device
    
#         add_room_or_device_view = AddRoomOrDeviceView(self._controller, title, 400, 400, tk.Toplevel(), main_view=self, tab_to_be_added_on_name=tab_name)
#         add_room_or_device_view.run()

#     def keep_refresh_tab_content(self):
#         """Refresh tab content periodically."""
#         if self._current_tab_full_name:
#             try:
#                 self._controller.show_tab_content(self._current_tab_full_name)
#             except Exception as e:
#                 print(f"Error refreshing tab content: {e}")
#         self._window.after(3000, self.keep_refresh_tab_content)  # Refresh every second

# # Comment on GPT use
# # Prompt: "I want a space initially show nothing, click on it a scroll down window shows up, 
# # it can be clicked to choose the option once the option clicked, the scroll window closed, 
# # the option shows on the space, I need a scroll control using scoll button on the mouse"
# class AddRoomOrDeviceView(View):
#     def __init__(self, controller, title, width, height, window_function, main_view=None, tab_to_be_added_on_name=None):
#         """Initialize the AddRoomOrDeviceView class.
#         Keyword arguments:
#         controller -- The controller that manages the interaction between the view and model
#         title(str) -- The title of the login window 
#         width(int) -- The width of the login window 
#         height(int) -- The height of the login window 
#         window_function -- The window function to create the login window
#         main_view -- The main view object
#         tab_name -- The name of the tab to add a device to
#         """
        
#         self._main_view = main_view
#         self._tab_to_be_added_on_name = tab_to_be_added_on_name
        
#         if self._tab_to_be_added_on_name is None:
            
#             # Add a room
#             self._options = ["Living Room", "Bedroom", "Kitchen"]
#             self._default_text = "Select a room type"
#             self._error_message = "Please select a room type!"
#             self._confirm_button_text = "Add Room"
#         else:
            
#             # Add Device
#             self._options = ["Television", "Lamp", "Refrigerator", "Air Conditioner", "Electric Kettle", "Bedside Lamp"]
#             self._default_text = "Select a device type"
#             self._error_message="Please select a device type!"
#             self._confirm_button_text="Add Device"
        
#         super().__init__(controller, title, width, height, window_function)
        
#     def _setup_ui(self):
        
#         # Selected option 
#         self._selected_option = tk.StringVar(value=self._default_text)

#         # Main dropdown display space 
#         self._dropdown_space = tk.Label(
#             self._window,
#             textvariable=self._selected_option,
#             bg="lightgray",
#             font=("Arial", 12),
#             width=80,
#             height=2,
#             relief="solid",
#             anchor="w"
#         )
#         self._dropdown_space.pack(pady=20)
#         self._dropdown_space.bind("<Button-1>", self.toggle_dropdown)

#         # Dropdown frame (initially hidden)
#         self._dropdown_frame = tk.Frame(self._window, bg="white", relief="solid", bd=1)
#         self._dropdown_visible = False

#         # Add a canvas and scrollbar for the dropdown options
#         self._canvas = tk.Canvas(self._dropdown_frame, bg="white")
#         self._scrollbar = tk.Scrollbar(self._dropdown_frame, orient=tk.VERTICAL, command=self._canvas.yview)
#         self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self._canvas.configure(yscrollcommand=self._scrollbar.set)
#         self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         # Frame inside the canvas for dropdown items
#         self._options_frame = tk.Frame(self._canvas, bg="white")
#         self._canvas.create_window((0, 0), window=self._options_frame, anchor="nw")

#         # Add options to the dropdown
#         self.add_options()

#         # Bind resizing to update the scrollable region
#         self._options_frame.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))

#         # Bind mouse wheel for scrolling
#         self._canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
#         # Add Room button
#         button_frame = ttk.Frame(self._window)
#         button_frame.pack(pady=100)  

#         add_room_button = ttk.Button(button_frame,text=self._confirm_button_text,command=self.handle_confirm)
#         add_room_button.grid(row=0, column=0, padx=10, pady=10)

#     def add_options(self):
#         """Add clickable options to the dropdown."""
#         for option in self._options:
#             option_label = tk.Label(
#                 self._options_frame,
#                 text=option,
#                 bg="white",
#                 font=("Arial", 12),
#                 anchor="w",
#                 padx=10
#             )
#             option_label.pack(fill="x", pady=2)
#             option_label.bind("<Button-1>", lambda e, opt=option: self.select_option(opt))
#             option_label.bind("<Enter>", lambda e: e.widget.configure(bg="lightblue"))
#             option_label.bind("<Leave>", lambda e: e.widget.configure(bg="white"))

#     def toggle_dropdown(self, event=None):
#         """Show or hide the dropdown menu."""
#         if self._dropdown_visible:
#             self._dropdown_frame.place_forget() # Hide the dropdown
#             self._dropdown_visible = False
#         else:
            
#             # Show the dropdown
#             self._dropdown_frame.place(x=self._dropdown_space.winfo_x(),
#                                        y=self._dropdown_space.winfo_y() + self._dropdown_space.winfo_height(),
#                                        width=self._dropdown_space.winfo_width(),
#                                        height=100)  # Set height to fit options
#             self._dropdown_visible = True

#     def select_option(self, option):
#         """Handle option selection."""
#         self._selected_option.set(option)  # Set the selected option
#         self.toggle_dropdown()  # Close the dropdown

#     def on_mousewheel(self, event):
#         """Scroll the canvas using the mouse wheel."""
#         self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
#     def handle_confirm(self):
#         """Handle adding a new room or a new device."""
        
#         selected = self._selected_option.get()
#         if selected == self._default_text or not selected:
#             messagebox.showerror(self._confirm_button_text, self._error_message)
            
#             return
        
#         try:
#             # Call the controller to add the room data
#             if self._tab_to_be_added_on_name is None:
                
#                 # Add a room
#                 self._controller.add_tab_button(selected)
#                 messagebox.showinfo("Add Room", f"{selected} added successfully!")
#             else:        
                
#                 # Call the controller to add the device data to the room
#                 success, message = self._controller.add_device(self._tab_to_be_added_on_name, selected)

#                 # Notify the user of success or failure
#                 if success:
#                     messagebox.showinfo("Add Device", f"{selected} added to {self._tab_to_be_added_on_name} successfully!")
#                 else:
#                     messagebox.showerror("Add Device", message) 
                    
#             self._window.destroy()  # Close the window on success
        
#         except ValueError as e:
#             messagebox.showerror(self._confirm_button_text, str(e))