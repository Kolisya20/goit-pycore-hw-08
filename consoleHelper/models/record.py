from models.field import Name, Phone, Birthday, Email
from datetime import datetime, timedelta

class Record:
    def __init__(self, name) -> None:
        self.name = Name(name)
        self.phones = []
        self.emails = []
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

    def add_email(self, email):
            email_obj = Email(email)
            self.emails.append(email_obj)    

    def edit_email(self, old_email, new_email):
        if not Email.validate(new_email):
            raise ValueError("Wrong format")
        
        for email_obj in self.emails:
            if email_obj.value == old_email:
                email_obj.value = new_email
                return True
        return False

    def find_email(self, email):
        for email_obj in self.emails:
            if email_obj.value == email:
                return email_obj
        return None
    
    def remove_email(self, email):
        for email_obj in self.emails:
            if email_obj.value == email:
                self.emails.remove(email_obj)
                return True
        return False

    def edit_email(self, old_email, new_email):
        if not Phone.validate_and_format(new_email):
            raise ValueError("Wrong format")
        
        for email_obj in self.phones:
            if email_obj.value == old_email:
                email_obj.value = new_email
                return True
        return False

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"
