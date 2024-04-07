import os

from interfaces import UserInterface
from exceptions import (UserDoesNotExistError,
                        UserAlreadyExistsError,
                        UpdateInfoNotUniqueError,
                        FieldDoesNotExistError)


class UserManager(UserInterface):

    def __init__(self, file_name):
        self.file_name = file_name
        self._create_if_not_exists()

    def _create_if_not_exists(self) -> None:
        print(os.path.abspath("main.py"))
        if not os.path.isfile(self.file_name):
            with open(self.file_name, 'w') as f:
                f.write("Full name, email, phone number\n")

    def _check_if_user_exists(
            self,
            first_name: str,
            last_name: str,
            email: str = "",
            phone_number: str = ""
    ) -> int | bool:

        with open(self.file_name) as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line = line.rstrip("\n").split(", ")
            if email == line[1]:
                return i
            if phone_number == line[2]:
                return i
            if " ".join([first_name, last_name]) == line[0]:
                return i
        return False

    def create(self, first_name: str, last_name: str, email: str, phone_number: str) -> str | None:
        if self._check_if_user_exists(first_name, last_name, email, phone_number):
            raise UserAlreadyExistsError
        else:
            user_data = [" ".join([first_name, last_name]), email, phone_number]
            user_str = ", ".join(user_data)
            with open(self.file_name, "a") as f:
                f.write(user_str + '\n')
            return "The user has been successfully created."

    def _delete_by_user_line(self, line_with_user: int) -> None:
        with open(self.file_name) as f:
            lines = f.readlines()

        with open(self.file_name, "w") as f:
            for i, line in enumerate(lines):
                if i == line_with_user:
                    continue
                f.write(line)

    def delete(self, first_name: str, last_name: str) -> str | None:
        line_with_user = self._check_if_user_exists(first_name, last_name)
        if not line_with_user:
            raise UserDoesNotExistError
        else:
            self._delete_by_user_line(line_with_user)
            return "User has been successfully deleted"

    def _read_user_by_user_line_or_param(self, user_param: str = "", user_line: str | int = "") -> str | None:
        with open(self.file_name, "r") as f:
            for i, line in enumerate(f.readlines()):
                line = line.rstrip("\n")
                if user_line:
                    if user_line == i:
                        return line
                else:
                    if user_param in line:
                        line = line.rstrip("\n")
                        info_list = line.split(", ")
                        for piece in info_list:
                            if piece == user_param:
                                return line

    def read(self, first_name: str, last_name: str) -> str | None:
        user_line = self._check_if_user_exists(first_name, last_name)
        if not user_line:
            raise UserDoesNotExistError
        else:
            return self._read_user_by_user_line_or_param(user_line=user_line)

    def read_all(self) -> str:
        with open(self.file_name) as f:
            content = f.read()
        return content

    def update(self, field_name: str, new_value: str, first_name: str, last_name: str) -> str | None:
        user_line = self._check_if_user_exists(first_name, last_name)
        if not user_line:
            raise UserDoesNotExistError

        # checking if there is a user in the file with the same new_value
        user_to_update_str = self._read_user_by_user_line_or_param(user_line=user_line)
        if isinstance(field_name, list):
            new_value = [value.capitalize() for value in new_value.split()]
            param = " ".join(new_value)
        else:
            param = new_value

        user_with_same_new_value_str = self._read_user_by_user_line_or_param(user_param=param)

        if user_with_same_new_value_str and user_to_update_str != user_with_same_new_value_str:
            raise UpdateInfoNotUniqueError

        # deleting the old string in the file and adding the one with updated info
        fields = ["first_name", "last_name", "email", "phone"]

        user_to_update_ls = user_to_update_str.split(", ")
        user_full_name = user_to_update_ls[0]
        all_user_info = user_full_name.split(" ")
        all_user_info.extend(user_to_update_ls[1:])

        if isinstance(new_value, list):
            all_user_info[0] = new_value[0]
            all_user_info[1] = new_value[1]

        elif field_name in fields:
            update_field_index = fields.index(field_name)
            all_user_info[update_field_index] = new_value

        else:
            raise FieldDoesNotExistError

        self.delete(first_name, last_name)

        first_name = all_user_info[0]
        last_name = all_user_info[1]
        email = all_user_info[2]
        phone = all_user_info[3]

        self.create(first_name, last_name, email, phone)
        return "The user has been successfully updated"
