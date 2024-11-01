from models.field import Name, Phone, Birthday
from datetime import datetime, timedelta

class Record:
    def __init__(self, name) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
    
    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                return True
        return False
    
    def edit_phone(self, old_phone, new_phone):
        if not Phone.validate(new_phone):
            raise ValueError("Phone number must contain exactly 10 digits.")
        
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone
                return True
        return False

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None
    
    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists.")

    def show_birthday(self):
        if self.birthday:
            return self.birthday
        else:
            return f"{self.name.value} has no birthday set."

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().date()
        next_birthdays = self.birthday.value.replace(year=today.year)
        if next_birthdays < today:
            next_birthdays = next_birthdays.replace(year=today.year + 1)
        return (next_birthdays - today).days

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"
