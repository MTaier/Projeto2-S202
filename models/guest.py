from datetime import datetime

class Guest:
    def __init__(self, name, email, phone=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at,
        }