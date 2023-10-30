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
    date_format = "%d.%m.%Y"
    def __init__(self, value):
        self.value = datetime.strptime(value, self.date_format).date()
    
    def __str__(self):
        return self.value.strftime(self.date_format)


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [] if not phone else [Phone(phone)]
        self.birthday = birthday if not birthday else Birthday(birthday)

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
        return f"Birthday added to contact {self.name}"

    def show_birthday(args, contacts):
        # Метод для виводу дня народження
        name = args[0]
        contact = contacts.find(name)
        if contact:
            return f"Birthday forrrrrr {contact.name.value}: {contact.birthday}" if contact.birthday else "Don't know the birthday."
        else:
            return f"Contact {name} does not exist."

    def __str__(self):
        bd_str = str(self.birthday) if self.birthday else "not set"
        phones_str = "; ".join(str(p) for p in self.phones) if self.phones else "not set"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bd_str}"


class AddressBook(UserDict):
    # def add_birthday(self, name, birthday):
    #     # Метод для додавання дня народження до існуючого контакту
    #     contact = self.data.get(name)
    #     if contact:
    #         contact.add_birthday(birthday)
    #     else:
    #         print(f"Contact {name} not found.")
    # # реалізація класу
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

    def get_birthdays_per_week(self):
        birthdays_week = defaultdict(list)
        current_date = datetime.today().date()
        
        for rec in self.data.values():
            name = str(rec.name)
            birthday = rec.birthday
            if not birthday:
                continue
            birthday_this_year = birthday.value.replace(year=current_date.year)
            days_difference = (birthday_this_year - current_date).days
            day_of_week = (current_date + timedelta(days=days_difference)).strftime("%A")
            
            if days_difference >= 0 and days_difference < 7:
                birthdays_week[day_of_week].append(name)

        for day, names in birthdays_week.items():
            return f"This week don't forget to wish your collegues a happy birthday. On {day}: {', '.join(names)}"
    
    def __str__(self) -> str:
        if not self.data:
            return "No records yet"
        return "\n".join(str(r) for r in self.data.values())
    

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
    name = args[0]
    phone = args[1]
    rec = contacts.get(name)
    if rec:
        rec.add_phone(phone)
        return f"Phone {phone} added to contact {name}"
    contacts.add_record(Record(name, phone=phone))
    
    return f"Contact {name} added with phone {phone}"


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
def add_birthday(args, contacts):
    name = args[0]
    birthday_str = args[1]
    rec = contacts.get(name)
    if rec:
        return rec.add_birthday(birthday_str)
    contacts.add_record(Record(name, birthday=birthday_str))
    return f"Contact {name} added with birthday {birthday_str}"

@input_error
def show_birthday(args, contacts):
    name = args[0]
    contact = contacts.find(name)
    if contact:
        return f"Birthday for {contact.name.value}: {contact.birthday}" if contact.birthday else "Don't know the birthday."
    else:
        return f"Contact {name} does not exist."


@input_error
def birthdays(contacts):
    birthdays_week = defaultdict(list)
    current_date = datetime.today().date()
    
    for rec in contacts.data.values():
        name = str(rec.name)
        birthday = rec.birthday
        if not birthday:
            continue
        birthday_this_year = birthday.value.replace(year=current_date.year)
        days_difference = (birthday_this_year - current_date).days
        day_of_week = (current_date + timedelta(days=days_difference)).strftime("%A")
        
        if days_difference >= 0 and days_difference < 7:
            birthdays_week[day_of_week].append(name)

    for day, names in birthdays_week.items():
        return f"This week don't forget to wish your collegues a happy birthday. On {day}: {', '.join(names)}"
         

@input_error
def show_all_contacts(contacts):
    return str(contacts)
    # if contacts:
    #     contact = ''
    #     for name, phone in contacts.items():
    #         contact += f"{name}: {phone}\n"
    #     return contact
    # else:
    #     return "No contacts found."


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        result = ""

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            result = add_contact(args, contacts)
        elif command == "change":
            result = change_username_phone(args, contacts)
        elif command == "phone":
            result = get_username_phone(args, contacts)
        elif command == "all":
            result = show_all_contacts(contacts)
        elif command == "add-birthday":
            result = add_birthday(args, contacts)
            # if len(args) < 2:
            #     print("Usage: add-birthday <contact_name> <birthday>")
            # else:
            #     contact_name = args[0]
            #     birthday = args[1]
            #     contacts.add_birthday(contact_name, birthday)
            #     print(f"Birthday added for {contact_name}.")
        elif command == "show-birthday":
            result = show_birthday(args, contacts)
            print(result)
        


        elif command == "birthdays":
            result = birthdays(contacts)
        else:
            result = "Invalid command."
        print(result)


if __name__ == "__main__":
    main()
