import re

from interfaces import ValidatorInterface


class Validator(ValidatorInterface):

    def validate_email(self, email: str) -> str | None:
        pattern = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        try:
            match = re.fullmatch(pattern, email.strip())
            if match:
                return match.group()
            else:
                raise ValueError("Email is not in the correct format")
        except ValueError as error:
            print(error)

    def validate_name(self, name: str) -> str | None:
        pattern = r"[A-Za-z]+"
        try:
            match = re.fullmatch(pattern, name.strip())
            if match:
                return match.group()
            else:
                raise ValueError("Name must contain only latin letters")
        except ValueError as error:
            print(error)

    def validate_phone_number(self, number: str) -> str | None:
        pattern = r"\+[0-9]{12}"
        try:
            match = re.fullmatch(pattern, number.strip())
            if match:
                return match.group()
            else:
                raise ValueError("Incorrect phone number")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    validator = Validator()
    print(validator.validate_name("Fb77jd9!8"))
    print(validator.validate_email("svitlaroza@gmailcom"))
    print(validator.validate_phone_number("+380993325832"))
