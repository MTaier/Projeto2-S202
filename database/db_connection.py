from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import CollectionInvalid

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.client = MongoClient('mongodb://localhost:27017/')
            cls._instance.db = cls._instance.client['hotel_management']
            cls._instance._setup_collections()
            cls._instance._create_indexes()
        return cls._instance

    def _setup_collections(self):
        # Define schema validation for guests
        guest_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "email", "phone", "document"],
                "properties": {
                    "name": {"bsonType": "string"},
                    "email": {"bsonType": "string", "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"},
                    "phone": {"bsonType": "string"},
                    "document": {"bsonType": "string"}
                }
            }
        }

        # Define schema validation for rooms
        room_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["number", "type", "price", "status"],
                "properties": {
                    "number": {"bsonType": "string"},
                    "type": {"enum": ["Standard", "Deluxe", "Suite"]},
                    "price": {"bsonType": "double", "minimum": 0},
                    "status": {"enum": ["available", "occupied", "maintenance"]}
                }
            }
        }

        # Define schema validation for reservations
        reservation_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["guest_id", "room_number", "check_in", "check_out", "status", "created_at"],
                "properties": {
                    "guest_id": {"bsonType": "objectId"},
                    "room_number": {"bsonType": "string"},
                    "check_in": {"bsonType": "date"},
                    "check_out": {"bsonType": "date"},
                    "status": {"enum": ["active", "completed", "cancelled"]},
                    "created_at": {"bsonType": "date"}
                }
            }
        }

        try:
            self.db.create_collection("guests", validator=guest_validator)
            self.db.create_collection("rooms", validator=room_validator)
            self.db.create_collection("reservations", validator=reservation_validator)
        except CollectionInvalid:
            pass  # Collections already exist

    def _create_indexes(self):
        # Indexes for guests collection
        self.db.guests.create_index([("email", ASCENDING)], unique=True)
        self.db.guests.create_index([("document", ASCENDING)], unique=True)

        # Indexes for rooms collection
        self.db.rooms.create_index([("number", ASCENDING)], unique=True)
        self.db.rooms.create_index([("status", ASCENDING)])

        # Indexes for reservations collection
        self.db.reservations.create_index([("guest_id", ASCENDING)])
        self.db.reservations.create_index([("room_number", ASCENDING)])
        self.db.reservations.create_index([("check_in", ASCENDING), ("check_out", ASCENDING)])
        self.db.reservations.create_index([("status", ASCENDING)])

    def get_database(self):
        return self.db