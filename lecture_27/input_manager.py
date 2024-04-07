from typing import Callable

from validators import Validator
from user_manager import UserManager
from exceptions import (PhoneValidationError,
                        EmailValidationError,
                        NameValidationError,
                        FieldDoesNotExistError,
                        UserDoesNotExistError,
                        UserAlreadyExistsError,
                        UpdateInfoNotUniqueError)


class InputManager:

    def __init__(self, validator: Validator, user_manager: UserManager):
        self.validator = validator
        self.user_manager = user_manager

    @staticmethod
    def _validate_input(input_prompt: str, validate_func: Callable) -> str:
        inp = input(input_prompt).lower()
        if validate_func(inp):
            return inp

    def _validate_name_input(self) -> tuple[str, str] | None:
        first_name = input("First name: ").strip().lower().capitalize()
        last_name = input("Last name: ").strip().lower().capitalize()
        if self.validator.validate_name(first_name) and self.validator.validate_name(last_name):
            return first_name, last_name

    def create(self) -> None:
        try:
            print("Enter the following details to create a user: ")
            first_name, last_name = self._validate_name_input()
            email = self._validate_input("Email: ", self.validator.validate_email)
            phone_number = self._validate_input("Phone number: ", self.validator.validate_phone_number)

            print(self.user_manager.create(first_name, last_name, email, phone_number))
        except (PhoneValidationError, EmailValidationError, NameValidationError, UserAlreadyExistsError) as error:
            print(error)

    def read(self) -> None:
        print("Enter the following details to view the full user's info: ")
        try:
            first_name, last_name = self._validate_name_input()
            user = self.user_manager.read(first_name, last_name)
            print(user)
        except (UserDoesNotExistError, EmailValidationError, NameValidationError, PhoneValidationError) as error:
            print(error)

    def delete(self) -> None:
        print("Enter the following details to delete a user: ")
        try:
            first_name, last_name = self._validate_name_input()
            print(self.user_manager.delete(first_name, last_name))
        except (UserDoesNotExistError, EmailValidationError, NameValidationError, PhoneValidationError) as error:
            print(error)

    def update(self) -> None:
        try:
            print("Enter the first and last names of the user you want to update:")
            first_name, last_name = self._validate_name_input()
            field = input("Enter the field you want to update(full name, email, phone number): ").lower()
            new_value = input("Enter the new value: ").lower()

            # new field value validation
            validate_field_value = self.validator.choose_validator(field)
            if not validate_field_value:
                raise FieldDoesNotExistError

            if "name" in field:
                first_last = new_value.split()
                for name in first_last:
                    validate_field_value(name.capitalize())
                field = ["first_name", "last_name"]
            else:
                validate_field_value(new_value)

            print(self.user_manager.update(
                field, new_value,
                first_name=first_name,
                last_name=last_name)
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

    def read_all(self) -> None:
        print(self.user_manager.read_all())
