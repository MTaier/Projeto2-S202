class Room:
    def __init__(self, number, type, price, status="available"):
        self.number = number
        self.type = type
        self.price = price
        self.status = status

    def to_dict(self):
        return {
            "number": self.number,
            "type": self.type,
            "price": self.price,
            "status": self.status
        }