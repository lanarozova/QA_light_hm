import re

from interfaces import UserInterface
from exceptions import (UserDoesNotExistError,
                        UserAlreadyExistsError,
                        UpdateInfoNotUniqueError,
                        FieldDoesNotExistError)

import os


class UserManager(UserInterface):

    def __init__(self, file_name):
        self.file_name = file_name
        self._create_if_not_exists()

    def _create_if_not_exists(self):
        print(os.path.abspath("main.py"))
        if not os.path.isfile(self.file_name):
            with open(self.file_name, 'w') as f:
                f.write("")
        else:
            print(os.path.abspath(self.file_name))

    def _check_if_user_exists(self, first_name="", last_name="", email="", phone_number=""):
        with open(self.file_name) as f:
            lines = f.readlines()

        for line in lines:
            if first_name and last_name:
                match = re.search(" ".join([first_name, last_name]), line)
                if match:
                    return True
            if email:
                match = re.search(email, line)
                if match:
                    return True
            if phone_number:
                match = re.search(phone_number, line)
                if match:
                    return True
        return False

    def create(self, first_name, last_name, email, phone_number):
        if self._check_if_user_exists(first_name, last_name, email, phone_number):
            raise UserAlreadyExistsError
        else:
            user_data = [" ".join([first_name, last_name]), email, phone_number]
            user_str = ", ".join(user_data)
            with open(self.file_name, "a") as f:
                f.write(user_str + '\n')
            return "The user has been successfully created."

    def _delete_by_user_parameter(self, user_param) -> None:
        line_to_delete = ""
        with open(self.file_name, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if user_param in line:
                    line_to_delete = i

        with open(self.file_name, "w") as f:
            for i, line in enumerate(lines):
                if i == line_to_delete:
                    continue
                f.write(line)

    def delete(self, first_name: str = "", last_name: str = "", email: str = "", phone_number: str = ""):
        if not self._check_if_user_exists(first_name, last_name, email, phone_number):
            raise UserDoesNotExistError
        else:
            param = ""
            if first_name and last_name:
                param = " ".join([first_name, last_name])
            elif email or phone_number:
                param = email if email else phone_number

            self._delete_by_user_parameter(param)
            return "User has been successfully deleted"

    def _read_user_by_param(self, user_param) -> str:
        with open(self.file_name, "r") as f:
            for line in f.readlines():
                line = line.rstrip("\n")
                match = None
                if user_param in line:
                    info_list = line.split(", ")
                    for piece in info_list:
                        match = re.fullmatch(user_param, piece)
                        if match:
                            return line

    def read(self, first_name: str = "", last_name: str = "", email: str = "", phone_number: str = ""):
        if not self._check_if_user_exists(first_name, last_name, email, phone_number):
            raise UserDoesNotExistError
        else:
            param = None
            if first_name and last_name:
                param = " ".join([first_name, last_name])
            if email or phone_number:
                param = email if email else phone_number
            user_line = self._read_user_by_param(param)
            return user_line

    def read_all(self):
        with open(self.file_name) as f:
            content = f.read()
        return content

    def update(self, field_name: str, new_value: str, first_name: str = "", last_name: str = "", email: str = ""):
        user_to_update_str = self._read_user_by_param(new_value)
        user_with_same_new_value_str = self._read_user_by_param(new_value)

        if user_with_same_new_value_str == user_to_update_str:
            raise UpdateInfoNotUniqueError

        # deleting the old string in the file and adding the one with updated info
        self.delete(first_name, last_name, email)
        fields = ["first_name", "last_name", "email", "phone"]
        field_name = field_name.strip().lower()
        if field_name in fields:
            update_field_index = fields.index(field_name)
            user_to_update_ls = user_to_update_str.split(", ")
            user_full_name = user_to_update_ls[0]
            all_user_info = user_full_name.split(" ")
            all_user_info.extend(user_to_update_ls[1:])

            all_user_info[update_field_index] = new_value

            first_name = all_user_info[0]
            last_name = all_user_info[1]
            email = all_user_info[2]
            phone = all_user_info[3]

            self.create(first_name, last_name, email, phone)
            return "The user has been successfully updated"
        else:
            raise FieldDoesNotExistError

#
if __name__ == "__main__":
    line = "Lana Lisova, test@gmail.com, 380997865471"
    match = re.search("380997865471", line)
    print(match)
