from collections import UserDict
from datetime import datetime, timedelta
from collections import defaultdict 

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, value):
        if value is not None and value.strip():  # Перевірка, що ім'я не є пустим рядком або None
            super().__init__(value)
        else:
            raise ValueError("Name is required")

class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if Phone.is_valid_phone_number(value):
            super().__init__(value)
    def is_valid_phone_number(phone_number):
        # Перевірка чи номер телефону має 10 цифр
        return phone_number.isdigit() and len(phone_number) == 10

class Birthday(Field):
    def __init__(self, birthday = ''):
        self.birthday = birthday

class Record:
    def __init__(self, name, birthday=''):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    # реалізація класу
    def add_phone(self, phone_number):
        # Метод для додавання об'єкта Phone до списку phones
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        # Метод для видалення об'єкта Phone зі списку phones
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_number, new_phone_number):
        # Метод для редагування номера телефону
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number

    def find_phone(self, phone_number):
        # Метод для пошуку об'єкта Phone за номером телефону
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def add_birthday(self, birthday):
        # Метод для додавання дня народження
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        # Метод для виводу дня народження
        return f"Birthday for {self.name.value}: {self.birthday.birthday}" if self.birthday else "Don't know the birthday."

     


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_birthday(self, name, birthday):
        # Метод для додавання дня народження до існуючого контакту
        contact = self.data.get(name)
        if contact:
            contact.add_birthday(birthday)
        else:
            print(f"Contact {name} not found.")
    # реалізація класу
    def add_record(self, record):
        # Метод для додавання запису до адресної книги
        self.data[record.name.value] = record

    def find(self, name):
        # Метод для пошуку запису за ім'ям
        
            record = self.data.get(name)
            
            return record 

    def delete(self, name):
        # Метод для видалення запису за ім'ям
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(users):
        birthdays_week = defaultdict(list)
        current_date = datetime.today().date()
        
        for user in users:
            name = user["name"]
            birthday = user["birthday"].date()
            birthday_this_year = birthday.replace(year=current_date.year)
            days_difference = (birthday_this_year - current_date).days
            day_of_week = (current_date + timedelta(days=days_difference)).strftime("%A")
            
            if days_difference >= 0 and days_difference < 7:
                birthdays_week[day_of_week].append(name)

        for day, names in birthdays_week.items():
            print(f"This week don't forget to wish your collegues a happy birthday. On {day}: {', '.join(names)}")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return f"KeyError: {str(e)}"
        except Exception as e:
            return f"An error occurred: {str(e)}"    

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_username_phone(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return f"Phone number updated for {name}."
    else:
        return f"Contact {name} does not exist."

@input_error
def get_username_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return f"Phone number for {name}: {contacts[name]}"
    else:
        return f"Contact {name} does not exist."

@input_error
def show_all_contacts(contacts):
    if contacts:
        contact = ''
        for name, phone in contacts.items():
            contact += f"{name}: {phone}\n"
        return contact
    else:
        return "No contacts found."



def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_username_phone(args, contacts))
        elif command == "phone":
            print(get_username_phone(args, contacts))
        elif command == "all":
            print(show_all_contacts(contacts))  
        elif command == "add-birthday":
            if len(args) < 2:
                print("Usage: add-birthday <contact_name> <birthday>")
            else:
                contact_name = args[0]
                birthday = args[1]
                contacts.add_birthday(contact_name, birthday)
                print(f"Birthday added for {contact_name}.")
        elif command == "show-birthday":
            contact = contacts.find(args[0])
            if contact:
                birthday_info = contact.show_birthday()
                print(birthday_info)
            else:
                print(f"Contact {args[0]} not found.")
        elif command == "birthdays":
            contacts.get_birthdays_per_week()
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
