from datetime import datetime

class Reservation:
    def __init__(self, guest_id, room_number, check_in, check_out, status="active"):
        self.guest_id = guest_id
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "guest_id": self.guest_id,
            "room_number": self.room_number,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "status": self.status,
            "created_at": self.created_at
        }