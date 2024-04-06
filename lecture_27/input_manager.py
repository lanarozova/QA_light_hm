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
        self.current_first_name = ""
        self.current_last_name = ""

    @staticmethod
    def _validate_input(input_prompt, validate_func):
        inp = input(input_prompt).lower()
        if validate_func(inp):
            return inp

    def validate_name_input(self):
        first_name = input("First name: ").strip().lower().capitalize()
        last_name = input("Last name: ").strip().lower().capitalize()
        if self.validator.validate_name(first_name) and self.validator.validate_name(last_name):
            return first_name, last_name

    def create(self):
        try:
            print("Enter the following details to create a user: ")
            first_name, last_name = self.validate_name_input()
            email = self._validate_input("Email: ", self.validator.validate_email)
            phone_number = self._validate_input("Phone number: ", self.validator.validate_phone_number)

            if all([first_name, last_name, email, phone_number]):

                user = UserTemplate(
                    first_name=first_name.capitalize(),
                    last_name=last_name.capitalize(),
                    email=email,
                    phone_number=phone_number
                )
                self.user_manager.create(user.first_name, user.last_name, user.email, user.phone_number)
                print("The user has been successfully created.")
        except (PhoneValidationError, EmailValidationError, NameValidationError, UserAlreadyExistsError) as error:
            print(error)
    #
    # def _validate_optional_input(self, func):
    #     inp = input("Enter first and last name OR email OR phone_number: ")
    #     inp = inp.strip()
    #     first_last = inp.split(" ")
    #     if inp.isnumeric() and self.validator.validate_phone_number(inp):
    #         return func(phone_number=inp)
    #     elif len(first_last) > 1:
    #         if self.validator.validate_name(first_last[0]) and self.validator.validate_name(first_last[1]):
    #             first_name = first_last[0].lower().capitalize()
    #             last_name = first_last[1].lower().capitalize()
    #             return func(first_name=first_name, last_name=last_name)
    #     elif self.validator.validate_email(inp):
    #         return func(email=inp.lower())
    #     else:
    #         return "Input datum does not fit either name, phone number or email requirements"

    def read(self):
        print("Enter the following details to view the full user's info: ")
        first_name, last_name = self.validate_name_input()
        try:
            user = self.user_manager.read(first_name.capitalize(), last_name.capitalize())
            print(user)
        except (UserDoesNotExistError, EmailValidationError, NameValidationError, PhoneValidationError) as error:
            print(error)

    def delete(self):
        print("Enter the following details to delete a user: ")
        first_name, last_name = self.validate_name_input()
        try:
            print(self.user_manager.delete(first_name, last_name))
        except (UserDoesNotExistError, EmailValidationError, NameValidationError, PhoneValidationError) as error:
            print(error)

    def update(self):
        try:
            print("Fields that can be updated: full name, email, phone number.")
            print("Enter the first and last names of the user you want to update:")
            first_name, last_name = self.validate_name_input()
            field = input("Enter the field you want to update: ").lower()
            new_value = input("Enter the new value: ").lower()

            # new field value validation
            validate_field_value = self.validator.choose_validator(field)
            if not validate_field_value:
                raise FieldDoesNotExistError

            if "name" in field:
                first_last = new_value.split()
                for name in first_last:
                    validate_field_value(name.capitalize())
            else:
                validate_field_value(new_value)

            print(self.user_manager.update(
                field, new_value,
                first_name=first_name.capitalize(),
                last_name=last_name.capitalize())
            )

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
