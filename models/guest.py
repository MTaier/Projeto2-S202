from datetime import datetime

class Guest:
    def _init_(self, name, email, phone, document):
        self.name = name
        self.email = email
        self.phone = phone
        self.document = document

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "document": self.document
            }