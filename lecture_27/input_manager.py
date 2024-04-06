from typing import NamedTuple


from validators import Validator
from user_manager import UserManager
from exceptions import (PhoneValidationError,
                        EmailValidationError,
                        NameValidationError,
                        FieldDoesNotExistError,
                        UserDoesNotExistError,
                        UserAlreadyExistsError,
                        UpdateInfoNotUniqueError)


class UserTemplate(NamedTuple):
    first_name: str
    last_name: str
    email: str
    phone_number: str


class InputManager:

    def __init__(self, validator: Validator, user_manager: UserManager):
        self.validator = validator
        self.user_manager = user_manager

    @staticmethod
    def _validate_input( input_prompt, validate_func):
        inp = input(input_prompt).lower()
        if validate_func(inp):
            return inp

    def create(self):
        try:
            first_name = self._validate_input("Enter first name: ", self.validator.validate_name).capitalize()
            last_name = self._validate_input("Enter last name: ", self.validator.validate_name).capitalize()
            email = self._validate_input("Enter email: ", self.validator.validate_email)
            phone_number = self._validate_input("Enter phone number: ", self.validator.validate_phone_number)

            if all([first_name, last_name, email, phone_number]):

                user = UserTemplate(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number
                )
                self.user_manager.create(user.first_name, user.last_name, user.email, user.phone_number)
                print("The user has been successfully created.")
        except (PhoneValidationError, EmailValidationError, NameValidationError, UserAlreadyExistsError) as error:
            print(error)

    def _validate_optional_input(self, func):
        inp = input("Enter first and last name OR email OR phone_number: ")
        inp = inp.strip()
        first_last = inp.split(" ")
        if inp.isnumeric() and self.validator.validate_phone_number(inp):
            return func(phone_number=inp)
        elif len(first_last) > 1:
            if self.validator.validate_name(first_last[0]) and self.validator.validate_name(first_last[1]):
                first_name = first_last[0].lower().capitalize()
                last_name = first_last[1].lower().capitalize()
                return func(first_name=first_name, last_name=last_name)
        elif self.validator.validate_email(inp):
            return func(email=inp.lower())
        else:
            return "Input datum does not fit either name, phone number or email requirements"

    def read(self):
        try:
            users = self._validate_optional_input(self.user_manager.read)
            print(users)
        except (UserDoesNotExistError, EmailValidationError, NameValidationError, PhoneValidationError) as error:
            print(error)

    def delete(self):
        try:
            print(self._validate_optional_input(self.user_manager.delete))
        except (UserDoesNotExistError, EmailValidationError, NameValidationError, PhoneValidationError) as error:
            print(error)

    def update(self):
        try:
            print("Fields that can be updated: full name, email, phone number")
            user_inp = input("Enter the first and last name OR email of the user you want to update: ").strip().split()
            field = input("Enter the field you want to update: ").lower()
            new_value = input("Enter the new value: ").lower()

            validate_name = self.validator.validate_name
            validate_email = self.validator.validate_email

            # new field value validation
            validate_field_value = self.validator.choose_validator(field)
            is_field_validated = False

            first_last = new_value.split()
            if "name" in field:
                temp = []
                for name in first_last:
                    temp.append(validate_field_value(name.capitalize()))
                is_field_validated = all(temp)
            else:
                is_field_validated = validate_field_value(new_value)

            if is_field_validated:
                if len(user_inp) > 1:
                    first_name = user_inp[0].capitalize()
                    last_name = user_inp[1].capitalize()
                    if validate_name(first_name) and validate_name(last_name):
                        print(self.user_manager.update(field, new_value, first_name=first_name, last_name=last_name))
                else:
                    email = user_inp[0]
                    if validate_email(email):
                        print(self.user_manager.update(field, new_value, email=email))

        except (
                UserDoesNotExistError,
                UserAlreadyExistsError,
                UpdateInfoNotUniqueError,
                EmailValidationError,
                NameValidationError,
                FieldDoesNotExistError
                ) as error:
            print(error)

    def read_all(self):
        print(self.user_manager.read_all())
