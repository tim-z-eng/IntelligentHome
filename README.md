# **IntelligentHome v1.0**

## **Table of Contents**
1. [Introduction](#introduction)
2. [Project Summary](#project-summary)
3. [Implementation Details](#implementation-details)
4. [Features](#features)
5. [Project Structure](#project-structure)
6. [Requirements](#requirements)
7. [Installation](#installation)
8. [Usage](#usage)
   - [Login](#login)
   - [Register as User](#register-as-user)
   - [Register as Admin](#register-as-admin)
   - [Room Management](#room-management)
   - [Device Management](#device-management)
   - [Temperature Control Logic](#temperature-control-logic)
9. [Data Management](#data-management)
10. [Testing](#testing)
11. [License](#license)

---

## **Introduction**
The *IntelligentHome* system is a prototype smart home controller designed to manage rooms, devices, and user access levels through an integrated, centralized platform. Implemented in Python and structured using a Model-View-Controller (MVC) pattern, the system enables the addition and configuration of rooms (Kitchen, Living Room, Bedroom), the control of various devices (Television, Lamp, Bedside Lamp, Refrigerator, Electric Kettle, Air Conditioner), and the maintenance of comfortable room temperatures using autonomous control logic.

The key features include:
- Secure user authentication.
- Persistent data storage using JSON files.
- Background temperature management.
- Role-based operations: MASTER, Admin, and User.

While only one room is visible at a time, all rooms continue to operate and update in real-time. Device states and temperature adjustments simulate realistic smart home operations.

---

## **Project Summary**
The *IntelligentHome* system includes the following functionalities:

### **1. User Authentication and Access Control**
- Three roles: MASTER, Admin, and User.
- **MASTER**: Full control, including registering Admin and User accounts, adding/removing rooms and devices, and managing device states.
- **Admin**: Can register User accounts, add and remove rooms, and manage devices within existing rooms.
- **User**: Can toggle device states (ON/OFF) and view room/device information.

### **2. Room and Device Management**
- Add, remove, and manage rooms (Kitchen, Bedroom, Living Room).
- Populate rooms with devices (TV, Lamp, Air Conditioner, etc.).
- Device constraints include compatibility with rooms and limits on device counts.

### **3. Device State Control and Temperature Dynamics**
- Devices toggle ON/OFF or adjust multiple states.
- Two-State Devices (Lamp, TV) contribute heat when ON.
- Multi-State Devices (Air Conditioner) provide heating and cooling levels.

### **4. Concurrent Room Temperature Management**
- All rooms operate in dedicated threads.
- Real-time updates ensure the latest temperature and device states are reflected.

### **5. Persistent Data Storage**
- User accounts and device/room structures are saved in JSON files.
- Files:
  - `users.json`: User credentials and access levels.
  - `tabs.json`: Rooms, devices, and configurations.

### **6. Temperature Control Logic**
- Uses a finite-state-machine (FSM) to automatically heat or cool rooms.
- Maintains temperatures within predefined thresholds (upper/lower bounds).

---

## **Implementation Details**

### **User Authentication and Access Control**
Authentication starts by loading credentials from `users.json` with the `AccessLevel` enumeration:
- **MASTER**: Access Level 3. Full control of the system:
  - Register Admin and User accounts.
  - Add and remove rooms.
  - Add, remove, and toggle devices.
  - Manage all device states and temperature control logic.
- **Admin**: Access Level 2. Restricted control:
  - Register User accounts.
  - Add and remove rooms.
  - Add, remove, and toggle devices within rooms.
- **User**: Access Level 1. Basic usage:
  - Toggle device states (ON/OFF).
  - View room and device information.

Input validation ensures no empty or duplicate entries, and permissions strictly respect the role hierarchy.

---

### **Room and Device Management**
Rooms and devices are loaded from `tabs.json` at startup. MASTER users can add or remove rooms/devices dynamically.

- **Adding Rooms**: Prompts the user to select a room type.
- **Adding Devices**: Devices are validated against room compatibility.
- **Removing Devices**: Devices are removed from the room and JSON is updated.

Admins can add/remove devices within existing rooms but cannot add new rooms.

---

### **Device State Control**
Devices are categorized as:
1. **Two-State Devices (Lamp, TV, etc.)**: ON/OFF states contribute to room heat.
2. **Multi-State Devices (Air Conditioner)**: Supports 11 states (5 cooling, 5 heating, OFF).
3. **Central Air Conditioner**: Automatically adjusts room temperature based on FSM logic.

Users can toggle device states, while MASTER and Admin roles have full device control.

---

### **Concurrent Room Temperature Management**
Each room runs its temperature calculations in a separate thread. Real-time updates ensure that switching between tabs reflects the latest state.

---

## **Features**
- **MASTER Role**: Full system control.
- **Admin Role**: Room and device management, register Users.
- **User Role**: Basic control to toggle device states.
- Room management (Add Room, Remove Room).
- Device management (Add Device, Remove Device, Toggle States).
- Real-time temperature adjustment using FSM-based logic.

---

## **Project Structure**
```
INTELLIGENTHOME-1.0/
│
├── controller/
│   └── controller.py
│
├── database/
│   ├── tabs.json
│   └── users.json
│
├── images/
│   └── UBC.png
│
├── model/
│   ├── electrical_device_model.py
│   ├── main_model.py
│   ├── room_model.py
│   └── user_model.py
│
├── test/
│   ├── __init__.py
│   ├── test_controller.py
│   ├── test_electrical_device_model.py
│   ├── test_main_model.py
│   ├── test_room_model.py
│   └── test_user_model.py
│
├── utils/
│   ├── config.py
│   └── enums.py
│
├── view/
│   ├── base_view.py
│   ├── login_view.py
│   └── main_view.py
│
├── .gitignore
├── LICENSE
├── main.py
└── README.md
```

---

## **Requirements**
- Python 3.8 or higher
- No external libraries required

---

## **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/IntelligentHome.git
   cd IntelligentHome-1.0
   ```
2. **Run the Application**:
   ```bash
   python main.py
   ```

---

## **Usage**

### **Login**
- **MASTER**: Full access.
- **Example MASTER credentials**: Username `1`, Password `1`.

### **Register as User**
- Admins or MASTER can register User accounts with limited privileges.

### **Register as Admin**
- MASTER users can register Admin accounts.

### **Room Management**
- **MASTER**: Add rooms.
- **Admin**: View rooms.
- **User**: View rooms.

### **Device Management**
- **MASTER**: Add, remove, and toggle device states.
- **Admin**: Add, remove, and toggle device states.
- **User**: Toggle device states ON/OFF for two state device, change the power level for Air Conditioner.

### **Temperature Control Logic**
- Automatically heats or cools rooms within upper/lower bounds.

---

## **Data Management**
- **`users.json`**: Stores user credentials.
- **`tabs.json`**: Stores room and device configurations.

---

## **Testing**
Run unit tests using:
```bash
pytest test
```

---

## **License**
This project is licensed under the MIT License.

---

*This README was modified by ChatGPT.*
