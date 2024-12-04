from datetime import datetime
from models.guest import Guest
from models.room import Room
from models.reservation import Reservation
from repositories.guest_repository import GuestRepository
from repositories.room_repository import RoomRepository
from repositories.reservation_repository import ReservationRepository
from repositories.analytics_repository import AnalyticsRepository

class HotelService:
    def __init__(self):
        self.guest_repo = GuestRepository()
        self.room_repo = RoomRepository()
        self.reservation_repo = ReservationRepository()
        self.analytics_repo = AnalyticsRepository()

    def create_guest(self, name, email, phone, document):
        guest = Guest(name, email, phone, document)
        return self.guest_repo.create(guest)

    def create_room(self, number, type, price):
        room = Room(number, type, price)
        return self.room_repo.create(room)

    def make_reservation(self, guest_id, room_number, check_in, check_out):
        # Verify if room is available
        room = self.room_repo.find_by_number(room_number)
        if not room or room["status"] != "available":
            raise ValueError("Room is not available")

        # Create reservation
        reservation = Reservation(guest_id, room_number, check_in, check_out)
        self.reservation_repo.create(reservation)

        # Update room status
        self.room_repo.update_status(room_number, "occupied")
        
        return reservation

    def check_out(self, reservation_id):
        reservation = self.reservation_repo.find_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reservation not found")

        # Update reservation status
        self.reservation_repo.update_status(reservation_id, "completed")

        # Update room status
        self.room_repo.update_status(reservation["room_number"], "available")

    def get_available_rooms(self):
        return self.room_repo.find_available_rooms()

    def get_guest_reservations(self, guest_id):
        return self.reservation_repo.find_by_guest(guest_id)

    def get_active_reservations(self):
        return self.reservation_repo.find_active_reservations()

    # Analytics methods
    def get_occupancy_statistics(self):
        return self.analytics_repo.get_room_occupancy_stats()

    def get_revenue_report(self, start_date, end_date):
        return self.analytics_repo.get_revenue_by_room_type(start_date, end_date)

    def get_guest_statistics(self):
        return self.analytics_repo.get_guest_stay_statistics()

    def get_monthly_occupancy(self, year, month):
        return self.analytics_repo.get_monthly_occupancy_rate(year, month)