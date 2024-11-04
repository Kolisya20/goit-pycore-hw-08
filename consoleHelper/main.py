from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prettytable import PrettyTable
from models.address_book import AddressBook
from models.record import Record
from decorators import input_error
import pickle

COMMANDS = [
    "add", "change", "phone", "email", "all", "add-birthday", 
    "show-birthday", "birthdays", "add-email", "change-email",
    "delete-email", "find-email", "find-phone", "close", "exit", "hello"
]

command_completer = WordCompleter(COMMANDS, ignore_case=True)

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
        

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    save_data(book)
    return message

@input_error
def show_all_contacts(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    table = PrettyTable()
    table.field_names = ["Name", "Phones", "Emails", "Birthday"]
    for record in book.data.values():
        name = record.name.value
        phones = ', '.join(phone.value for phone in record.phones) if record.phones else "No phones"
        emails = ', '.join(email.value for email in record.emails) if record.emails else "No emails"
        birthday = record.show_birthday() if record.birthday else "No birthday"

        table.add_row([name, phones, emails, birthday])

    return str(table)

@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record and record.edit_phone(old_phone, new_phone):
        save_data(book)
        return "Phone number updated."
    return "Contact not found or old phone number does not match."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phones for {name}: {', '.join(phone.value for phone in record.phones)}"
    return "Contact not found."

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        save_data(book)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return record.show_birthday()
    return "Contact not found."

@input_error
def show_upcoming_birthdays(args, book: AddressBook):
    days_to_birthday = args[0]
    upcoming = book.get_upcoming_birthdays(days_to_birthday)
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(f"{record.name.value}: {record.show_birthday()}" for record in upcoming)

@input_error
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        save_data(book)
        return "Email added."
    return "Contact not found."

@input_error
def change_email(args, book: AddressBook):
    name, old_email, new_email = args
    record = book.find(name)
    if record and record.edit_email(old_email, new_email):
        save_data(book)
        return "Email updated."
    return "Contact not found or old email does not match."

@input_error
def delete_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record and record.remove_email(email):
        save_data(book)
        return "Email removed."
    return "Contact not found or email does not exist."

@input_error
def show_email(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Emails for {name}: {', '.join(email.value for email in record.emails)}"
    return "Contact not found."

@input_error
def find_by_email(args, book: AddressBook):
    email = args[0]
    results = book.find_by_email(email)
    if results:
        return "\n".join(str(record) for record in results)
    return "No contacts found with this email."

@input_error
def find_by_phone(args, book: AddressBook):
    phone = args[0]
    results = book.find_by_phone(phone)
    if results:
        return "\n".join(str(record) for record in results)
    return "No contacts found with this phone number."

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = prompt("Enter a command: ", completer=command_completer)
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_upcoming_birthdays(args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "change-email":
            print(change_email(args, book))
        
        elif command == "delete-email":
            print(delete_email(args, book))

        elif command == "find-email":
            print(find_by_email(args, book))

        elif command == "find-phone":
            print(find_by_phone(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
