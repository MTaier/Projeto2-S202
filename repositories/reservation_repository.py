from database.db_connection import DatabaseConnection

class ReservationRepository:
    def __init__(self):
        self.db = DatabaseConnection().get_database()
        self.collection = self.db.reservations

    def create(self, reservation):
        return self.collection.insert_one(reservation.to_dict())

    def find_by_id(self, reservation_id):
        return self.collection.find_one({"_id": reservation_id})

    def find_by_guest(self, guest_id):
        return list(self.collection.find({"guest_id": guest_id}))

    def find_by_room(self, room_number):
        return list(self.collection.find({"room_number": room_number}))

    def update_status(self, reservation_id, status):
        return self.collection.update_one(
            {"_id": reservation_id},
            {"$set": {"status": status}}
        )

    def find_active_reservations(self):
        return list(self.collection.find({"status": "active"}))