import tkinter as tk
from tkinter import messagebox
from controller.controller import AuthController
from utils.enums import AccessLevel

class View:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        self.window.mainloop()


class LoginView(View):
    def __init__(self, controller, title, width, height):
        super().__init__(controller)
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.setup_ui()

    def setup_ui(self):
        """Set up the GUI elements."""
        # Title
        tk.Label(self.window, text="Welcome", font=("Arial", 18)).pack(pady=10)

        # Username input
        tk.Label(self.window, text="Username").pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        # Password input
        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        # Buttons
        tk.Button(self.window, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.window, text="Add admin", command=self.add_admin).pack(pady=5)
        tk.Button(self.window, text="Add User", command=self.add_user).pack(pady=5)
        

    def login(self):
        """Handle login action."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.controller.login(username, password)
        if success:
            messagebox.showinfo("Login", message)
            self.window.destroy()  # Close the login window on success
        else:
            messagebox.showerror("Login", message)

    def add_user(self):
        """Open the Add User window."""
        add_user_view = AddUserView(self.controller, "Add New User", 400, 300)
        add_user_view.run()
        
    def add_admin(self):
        """Open the Add User window."""
        add_user_view = AddAdminView(self.controller, "Add New User", 400, 300)
        add_user_view.run()


class AddUserView(View):
    def __init__(self, controller, title, width, height):
        super().__init__(controller)
        self.window = tk.Toplevel()  # Create a new top-level window
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.setup_ui()

    def setup_ui(self):
        """Set up the GUI elements for adding a new user."""
        tk.Label(self.window, text="Add A New User", font=("Arial", 18)).pack(pady=10)

        # Admin username input
        tk.Label(self.window, text="Mater/Admin Username").pack()
        self.admin_username_entry = tk.Entry(self.window)
        self.admin_username_entry.pack()

        # Admin password input
        tk.Label(self.window, text="Mater/Admin Password").pack()
        self.admin_password_entry = tk.Entry(self.window, show="*")
        self.admin_password_entry.pack()

        # New username input
        tk.Label(self.window, text="New Username").pack()
        self.new_username_entry = tk.Entry(self.window)
        self.new_username_entry.pack()

        # New password input
        tk.Label(self.window, text="New Password").pack()
        self.new_password_entry = tk.Entry(self.window, show="*")
        self.new_password_entry.pack()

        # Buttons
        tk.Button(self.window, text="Register As User", command=self.register_as_user).pack(pady=5)

    def register_as_user(self):
        """Handle registration action."""
        admin_username = self.admin_username_entry.get()
        admin_password = self.admin_password_entry.get()
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        # Authenticate admin credentials
        admin_success, admin_message = self.controller.check_access(admin_username, admin_password, AccessLevel.User)
        if not admin_success:
            messagebox.showerror("Register", admin_message)
            return

        # Register new user
        success, message = self.controller.register(new_username, new_password, AccessLevel.User)
        if success:
            messagebox.showinfo("Register", message)
            self.window.destroy()  # Close the add user window on success
        else:
            messagebox.showerror("Register", message)

class AddAdminView(View):
    def __init__(self, controller, title, width, height):
        super().__init__(controller)
        self.window = tk.Toplevel()  # Create a new top-level window
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.setup_ui()

    def setup_ui(self):
        """Set up the GUI elements for adding a new user."""
        tk.Label(self.window, text="Add A New Admin", font=("Arial", 18)).pack(pady=10)

        # Admin username input
        tk.Label(self.window, text="Master Username").pack()
        self.admin_username_entry = tk.Entry(self.window)
        self.admin_username_entry.pack()

        # Admin password input
        tk.Label(self.window, text="Master Password").pack()
        self.admin_password_entry = tk.Entry(self.window, show="*")
        self.admin_password_entry.pack()

        # New username input
        tk.Label(self.window, text="New Adminname").pack()
        self.new_username_entry = tk.Entry(self.window)
        self.new_username_entry.pack()

        # New password input
        tk.Label(self.window, text="New Password").pack()
        self.new_password_entry = tk.Entry(self.window, show="*")
        self.new_password_entry.pack()

        # Buttons
        tk.Button(self.window, text="Register As Admin", command=self.register_as_admin).pack(pady=5)

    def register_as_admin(self):
        """Handle registration action."""
        admin_username = self.admin_username_entry.get()
        admin_password = self.admin_password_entry.get()
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        # Authenticate admin credentials
        access_success, access_message = self.controller.check_access(admin_username, admin_password, AccessLevel.Admin)
        if not access_success:
            messagebox.showerror("Register", access_message)
            return

        # Register new user
        success, message = self.controller.register(new_username, new_password, AccessLevel.Admin)
        if success:
            messagebox.showinfo("Register", message)
            self.window.destroy()  # Close the add user window on success
        else:
            messagebox.showerror("Register", message)

class MainView(View):
    def __init__(self, controller, title, width, height):
        super().__init__(controller)
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.setup_ui()

    def setup_ui(self):
        # Create a main frame
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        # Create a frame for side tabs
        self.tab_frame = tk.Frame(self.main_frame, bg="lightgray", width=100)
        self.tab_frame.pack(side="left", fill="y")

        # Create a frame for tab content
        self.content_frame = tk.Frame(self.main_frame, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Store tab buttons and frames
        self.tabs = {}
        self.current_tab = None

        tk.Button(self.main_frame, text="Add Room", command=self.add_room).pack(pady=5)
        # Create tabs
        self.add_tab("Tab 1", "Content for Tab 1")
        self.add_tab("Tab 2", "Content for Tab 2")
        self.add_tab("Tab 3", "Content for Tab 3")

        # Show the first tab
        self.show_tab("Tab 1")

    def add_tab(self, tab_name, tab_content):
        """Add a tab with a button and a content frame."""
        # Create a button for the tab
        tab_button = tk.Button(
            self.tab_frame,
            text=tab_name,
            relief="flat",
            bg="lightgray",
            activebackground="gray",
            command=lambda: self.show_tab(tab_name)
        )
        tab_button.pack(fill="x", pady=5)

        # Create a frame for the tab's content
        tab_frame = tk.Frame(self.content_frame, bg="white")

        # Add content to the tab's frame
        label = tk.Label(tab_frame, text=tab_content, bg="white", font=("Arial", 14))
        label.pack(pady=50)

        # Store the tab
        self.tabs[tab_name] = tab_frame

    def show_tab(self, tab_name):
        """Show the specified tab."""
        # Hide the current tab
        if self.current_tab:
            self.tabs[self.current_tab].pack_forget()

        # Show the new tab
        self.tabs[tab_name].pack(fill="both", expand=True)
        self.current_tab = tab_name

    def add_room(self):
        """Open the Add Room window."""
        add_room_view = AddRoom(self.controller, "Add Room", 700, 900)
        add_room_view.run()

# Comment on GPT use
# Prompt: "I want a space initially show nothing, click on it a scroll down window shows up, 
# it can be clicked to choose the option once the option clicked, the scroll window closed, 
# the option shows on the space, I need a scroll control using scoll button on the mouse"
class AddRoom(View):
    def __init__(self, controller, title, width, height):
        super().__init__(controller)
        self.window = tk.Toplevel()  # Create a new top-level window
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.setup_ui()

    def setup_ui(self):
        # Selected option (initially blank)
        self.selected_option = tk.StringVar(value="")

        # Main dropdown display space (clickable)
        self.dropdown_space = tk.Label(
            self.window,
            textvariable=self.selected_option,
            bg="lightgray",
            font=("Arial", 12),
            width=80,
            height=2,
            relief="solid",
            anchor="w"
        )
        self.dropdown_space.pack(pady=20)
        self.dropdown_space.bind("<Button-1>", self.toggle_dropdown)

        # Dropdown frame (initially hidden)
        self.dropdown_frame = tk.Frame(self.window, bg="white", relief="solid", bd=1)
        self.dropdown_visible = False

        # Add a canvas and scrollbar for the dropdown options
        self.canvas = tk.Canvas(self.dropdown_frame, bg="white")
        self.scrollbar = tk.Scrollbar(self.dropdown_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame inside the canvas for dropdown items
        self.options_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.options_frame, anchor="nw")

        # Add options to the dropdown
        self.options = [f"Option {i + 1}" for i in range(20)]
        self.add_options()

        # Bind resizing to update the scrollable region
        self.options_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def toggle_dropdown(self, event=None):
        """Show or hide the dropdown menu."""
        if self.dropdown_visible:
            self.dropdown_frame.place_forget()  # Hide the dropdown
            self.dropdown_visible = False
        else:
            # Show the dropdown
            self.dropdown_frame.place(x=self.dropdown_space.winfo_x(),
                                       y=self.dropdown_space.winfo_y() + self.dropdown_space.winfo_height(),
                                       width=self.dropdown_space.winfo_width(),
                                       height=150)  # Set height to fit options
            self.dropdown_visible = True

    def add_options(self):
        """Add clickable options to the dropdown."""
        for option in self.options:
            option_label = tk.Label(
                self.options_frame,
                text=option,
                bg="white",
                font=("Arial", 12),
                anchor="w",
                padx=10
            )
            option_label.pack(fill="x", pady=2)
            option_label.bind("<Button-1>", lambda e, opt=option: self.select_option(opt))
            option_label.bind("<Enter>", lambda e: e.widget.configure(bg="lightblue"))
            option_label.bind("<Leave>", lambda e: e.widget.configure(bg="white"))

    def select_option(self, option):
        """Handle option selection."""
        self.selected_option.set(option)  # Set the selected option
        self.toggle_dropdown()  # Close the dropdown

    def on_mousewheel(self, event):
        """Scroll the canvas using the mouse wheel."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")