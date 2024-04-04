from typing import NamedTuple

from validators import Validator
from user import UserManager


class UserTemplate(NamedTuple):
    first_name: str
    last_name: str
    email: str
    phone_number: str


class InputManager:

    def __init__(self, validator: Validator, user_manager: UserManager):
        self.validator = validator
        self.user_manager = user_manager

    def create(self):
        first_name = self.validator.validate_name(input("Enter first name: "))
        last_name = self.validator.validate_name(input("Enter last name: "))
        email = self.validator.validate_email(input("Enter email: "))
        phone_number = self.validator.validate_phone_number(input("Enter phone number: "))

        user = UserTemplate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )

        self.user_manager.create(user.first_name, user.last_name, user.email, user.phone_number)

# validators should return True or False only
    def _validate_optional_input(self, func):
        inp = input("Enter first and last name OR email OR phone_number")
        inp = inp.strip()
        first_last = inp.split(" ")
        if len(first_last) > 1:
            first_name = self.validator.validate_name(first_last[0])
            last_name = self.validator.validate_name(first_last[1])
            return func(first_name=first_name, last_name=last_name)
        elif self.validator.validate_email(inp) is not None:
            return func(email=self.validator.validate_email(inp))
        else:
            phone_number = self.validator.validate_phone_number(inp)
            if phone_number:
                return func(phone_number=phone_number)

    def read(self):
        return self._validate_optional_input(self.user_manager.read)

    def delete(self):
        return self._validate_optional_input(self.user_manager.delete)
