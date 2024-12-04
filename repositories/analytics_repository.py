from datetime import datetime
from database.db_connection import DatabaseConnection

class AnalyticsRepository:
    def __init__(self):
        self.db = DatabaseConnection().get_database()

    def get_room_occupancy_stats(self):
        """
        Get room occupancy statistics using aggregation pipeline
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "rooms": {"$push": "$number"}
                }
            }
        ]
        return list(self.db.rooms.aggregate(pipeline))

    def get_revenue_by_room_type(self, start_date, end_date):
        """
        Calculate revenue by room type for completed reservations
        """
        pipeline = [
            {
                "$match": {
                    "status": "completed",
                    "check_out": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$lookup": {
                    "from": "rooms",
                    "localField": "room_number",
                    "foreignField": "number",
                    "as": "room"
                }
            },
            {
                "$unwind": "$room"
            },
            {
                "$group": {
                    "_id": "$room.type",
                    "total_revenue": {
                        "$sum": "$room.price"
                    },
                    "reservations_count": {"$sum": 1}
                }
            }
        ]
        return list(self.db.reservations.aggregate(pipeline))

    def get_guest_stay_statistics(self):
        """
        Get statistics about guest stays using aggregation
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "guests",
                    "localField": "guest_id",
                    "foreignField": "_id",
                    "as": "guest"
                }
            },
            {
                "$unwind": "$guest"
            },
            {
                "$group": {
                    "_id": "$guest_id",
                    "guest_name": {"$first": "$guest.name"},
                    "total_stays": {"$sum": 1},
                    "average_stay_length": {
                        "$avg": {
                            "$subtract": ["$check_out", "$check_in"]
                        }
                    }
                }
            },
            {
                "$sort": {"total_stays": -1}
            }
        ]
        return list(self.db.reservations.aggregate(pipeline))

    def get_monthly_occupancy_rate(self, year, month):
        """
        Calculate monthly occupancy rate
        """
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        pipeline = [
            {
                "$match": {
                    "check_in": {"$lt": end_date},
                    "check_out": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": "$room_number",
                    "days_occupied": {
                        "$sum": {
                            "$divide": [
                                {
                                    "$subtract": [
                                        {"$min": ["$check_out", end_date]},
                                        {"$max": ["$check_in", start_date]}
                                    ]
                                },
                                86400000  # Convert milliseconds to days
                            ]
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_occupancy": {
                        "$avg": "$days_occupied"
                    }
                }
            }
        ]
        return list(self.db.reservations.aggregate(pipeline))