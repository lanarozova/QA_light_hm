from typing import NamedTuple

from interfaces import UserInterface

import os


class UserManager(UserInterface):

    def __init__(self, file_name):
        self.file_name = file_name
        self._create_if_not_exists()

    def _create_if_not_exists(self):
        if not os.path.isfile(self.file_name):
            with open(self.file_name, 'w'):
                pass

    def _check_if_user_exists(self, first_name="", last_name="", email="", phone_number=""):
        if first_name and last_name:
            with open(self.file_name) as f:
                for line in f.readlines():
                    if first_name in line and last_name in line:
                        return True
        elif email or phone_number:
            with open(self.file_name) as f:
                for line in f.readlines():
                    if email in line or phone_number in line:
                        return True
        return False

    def create(self, first_name, last_name, email, phone_number):
        if self._check_if_user_exists(first_name, last_name, email, phone_number):
            raise ValueError("Such user already exist")
        else:
            user_data = [" ".join([first_name, last_name]), email, phone_number]
            user_str = ", ".join(user_data)
            with open(self.file_name, "a") as f:
                f.write(user_str + '\n')

    def _delete_by_user_parameter(self, user_param) -> None:
        line_to_delete = ""
        lines = ""
        with open(self.file_name, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if user_param in line:
                    line_to_delete = i

        with open(self.file_name, "w") as f:
            for i, line in enumerate(lines):
                if i == line_to_delete:
                    continue

    def _read_user_by_param(self, user_param) -> str | None:
        with open(self.file_name, "r") as f:
            for line in f.readlines():
                if user_param in line:
                    return line

    def delete(self, first_name: str = "", last_name: str = "", email: str = "", phone_number: str = ""):
        try:
            if first_name and last_name:
                if self._check_if_user_exists(first_name=first_name, last_name=last_name):
                    self._delete_by_user_parameter(" ".join([first_name, last_name]))
                    return "User deleted"
            elif email or phone_number:
                if self._check_if_user_exists(email=email, phone_number=phone_number):
                    param = email if email else phone_number
                    self._delete_by_user_parameter(param)
                    return "User deleted"
            else:
                raise TypeError("First name and last name are required")
        except TypeError as error:
            print(error)

    def read(self, first_name: str = "", last_name: str = "", email: str = "", phone_number: str = ""):
        if first_name and last_name:
            if self._check_if_user_exists(first_name=first_name, last_name=last_name):
                param =  " ".join([first_name, last_name])
                return self._read_user_by_param(param)
        if email or phone_number:
            if self._check_if_user_exists(email=email, phone_number=phone_number):
                param = email if email else phone_number
                return self._read_user_by_param(param)


    # def update(self, first_name, last_name, field_name, new_value):
    #     with open(self.file_name) as f:
    #         for line in f.readlines():
    #             if
    #                 return line
    #     return False


if __name__ == "__main__":

    class Person(NamedTuple):
        first_name: str
        last_name: str
        email: str
        phone_number: str


    person = Person(first_name="Oleg", last_name="hjbuygvgy", email="fdrd@gm.com", phone_number="+380993345832")

    users = UserManager("users.txt")

    # users.create(person.first_name, person.last_name, person.email, person.phone_number)
    print(users.delete(first_name=person.first_name, last_name="hjbuygvgy"))


    # def main():
    #     input = input()
    #     if input == "create":
    #         # ask for inpur of info
    #         persons.create()
    #     elif input == "update":
    #         persons.update()
    #     elif input == "delete"
