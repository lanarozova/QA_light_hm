from input_manager import InputManager
from user_manager import UserManager
from validators import Validator


def main(filepath):
    user_manager = UserManager(filepath)
    validator = Validator()
    input_manager = InputManager(validator, user_manager)

    while True:
        print("Enter the command: ")
        user_command = input('>>>').strip().lower()

        commands = {
            "create": input_manager.create,
            "read": input_manager.read,
            "update": input_manager.update,
            "delete": input_manager.delete,
            "readall": input_manager.read_all
        }

        if user_command in commands:
            func = commands[user_command]
            func()
        elif user_command == 'exit':
            print('Exiting')
            break
        else:
            print('Unsupported command')


if __name__ == "__main__":
    main("test.txt")
