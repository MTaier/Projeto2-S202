from datetime import datetime
from services.hotel_service import HotelService

def main():
    hotel_service = HotelService()

    try:
        # Create a guest
        guest_id = hotel_service.create_guest(
            "John Doe",
            "john@example.com",
            "+1234567890",
            "ABC123"
        )
        print(f"Guest created with ID: {guest_id}")

        # Create multiple rooms with different types
        rooms = [
            ("101", "Standard", 100.00),
            ("201", "Deluxe", 150.00),
            ("301", "Suite", 250.00)
        ]
        
        for number, type_, price in rooms:
            hotel_service.create_room(number, type_, price)
            print(f"Room {number} ({type_}) created")

        # Make reservations
        check_in = datetime(2024, 1, 1)
        check_out = datetime(2024, 1, 5)
        
        reservation = hotel_service.make_reservation(
            guest_id,
            "101",
            check_in,
            check_out
        )
        print(f"Reservation created: {reservation.to_dict()}")

        # Generate analytics reports
        print("\nHotel Analytics:")
        
        # Room occupancy statistics
        occupancy_stats = hotel_service.get_occupancy_statistics()
        print("\nRoom Occupancy Statistics:")
        for stat in occupancy_stats:
            print(f"Status: {stat['_id']}, Count: {stat['count']}")

        # Revenue report
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        revenue_report = hotel_service.get_revenue_report(start_date, end_date)
        print("\nRevenue by Room Type:")
        for revenue in revenue_report:
            print(f"Room Type: {revenue['_id']}")
            print(f"Total Revenue: ${revenue['total_revenue']}")
            print(f"Reservations: {revenue['reservations_count']}")

        # Guest statistics
        guest_stats = hotel_service.get_guest_statistics()
        print("\nGuest Stay Statistics:")
        for stat in guest_stats:
            print(f"Guest: {stat['guest_name']}")
            print(f"Total Stays: {stat['total_stays']}")
            print(f"Average Stay Length: {stat['average_stay_length']} days")

        # Monthly occupancy rate
        occupancy_rate = hotel_service.get_monthly_occupancy(2024, 1)
        print("\nMonthly Occupancy Rate:")
        print(f"January 2024: {occupancy_rate[0]['average_occupancy']:.2f}%")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()