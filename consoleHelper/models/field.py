import re
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is a required field.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError()
        formatted_value = self.format_phone(value)
        super().__init__(formatted_value)

    @staticmethod
    def validate(phone):
        return phone.isdigit() and len(phone) == 10
    
    @staticmethod
    def format_phone(phone):
        return f"+38 ({phone[:3]}) {phone[3:6]} {phone[6:8]} {phone[8:]}"
    
class Email(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Email has wrong format. Please check")
        super().__init__(value)

    @staticmethod
    def validate(email):
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        if not pattern.match(email):
            raise ValueError("Wrong format for email. Please provide a valid email address.")
        return email
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

