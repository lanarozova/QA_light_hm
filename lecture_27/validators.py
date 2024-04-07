import re

from interfaces import ValidatorInterface
from exceptions import PhoneValidationError, EmailValidationError, NameValidationError


class Validator(ValidatorInterface):

    def choose_validator(self, param):
        if "name" in param:
            return self.validate_name
        elif "email" in param:
            return self.validate_email
        elif "phone" in param:
            return self.validate_phone_number

    def validate_email(self, email: str) -> bool:
        pattern = r"([A-Za-z0-9]+[.-_\+])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        match = re.fullmatch(pattern, email)
        if match:
            return True
        else:
            raise EmailValidationError

    def validate_name(self, name) -> bool:
        pattern = r"([A-Za-z]+)|([A-Za-z]+\-[A-Za-z])"
        match = re.fullmatch(pattern, name)
        if match:
            return True
        else:
            raise NameValidationError

    def validate_phone_number(self, number: str) -> bool:
        pattern = r"[0-9]{12}"
        match = re.fullmatch(pattern, number)
        if match:
            return True
        else:
            raise PhoneValidationError
