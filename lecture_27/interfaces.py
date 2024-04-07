from abc import ABC, abstractmethod


class UserInterface(ABC):

    @abstractmethod
    def create(self, first_name: str, last_name: str, email: str, phone_number: str) -> str | None:
        pass

    @abstractmethod
    def read(self, first_name: str, last_name: str) -> str | None:
        pass

    @abstractmethod
    def update(self, field_name: str, new_value: str, first_name: str, last_name: str) -> str | None:
        pass

    @abstractmethod
    def delete(self, first_name: str, last_name: str) -> str | None:
        pass


class ValidatorInterface(ABC):

    @abstractmethod
    def validate_name(self, name: str) -> bool:
        pass

    def validate_email(self, email: str) -> bool:
        pass

    def validate_phone_number(self, phone_number: str) -> bool:
        pass
