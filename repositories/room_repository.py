from database.db_connection import DatabaseConnection

class RoomRepository:
    def __init__(self):
        self.db = DatabaseConnection().get_database()
        self.collection = self.db.rooms

    def create(self, room):
        return self.collection.insert_one(room.to_dict())

    def find_by_number(self, room_number):
        return self.collection.find_one({"number": room_number})

    def find_available_rooms(self):
        return list(self.collection.find({"status": "available"}))

    def update_status(self, room_number, status):
        return self.collection.update_one(
            {"number": room_number},
            {"$set": {"status": status}}
        )

    def find_all(self):
        return list(self.collection.find())