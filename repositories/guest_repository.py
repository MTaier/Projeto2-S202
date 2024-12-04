from database.db_connection import DatabaseConnection

class GuestRepository:
    def __init__(self):
        self.db = DatabaseConnection().get_database()
        self.collection = self.db.guests

    def create(self, guest):
        return self.collection.insert_one(guest.to_dict())

    def find_by_id(self, guest_id):
        return self.collection.find_one({"_id": guest_id})

    def find_all(self):
        return list(self.collection.find())

    def update(self, guest_id, guest_data):
        return self.collection.update_one(
            {"_id": guest_id},
            {"$set": guest_data}
        )

    def delete(self, guest_id):
        return self.collection.delete_one({"_id": guest_id})