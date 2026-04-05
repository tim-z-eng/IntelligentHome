import json
import os

class MainModel:
    def __init__(self):
        # Path to the JSON database
        self.db_path = os.path.join("database", "room.json")
        self.rooms = self.load_rooms()

    def load_rooms(self):
        raise(NotImplementedError)