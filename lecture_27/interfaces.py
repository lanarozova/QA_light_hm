from abc import ABC, abstractmethod


class UserInterface(ABC):

    @abstractmethod
    def create(self, first_name: str, last_name: str, email: str, phone_number: str) -> None:
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self, field_name, new_value, first_name="", last_name="", email=""):
        pass

    @abstractmethod
    def delete(self, first_name: str = "", last_name: str = "", email: str = "", phone: str = ""):
        pass


class ValidatorInterface(ABC):

    @abstractmethod
    def validate_name(self, name: str) -> bool:
        pass

    def validate_email(self, email: str) -> bool:
        pass

    def validate_phone_number(self, phone_number: str) -> bool:
        pass
