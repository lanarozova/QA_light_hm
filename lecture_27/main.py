
from input_manager import InputManager
from user import UserManager
from validators import Validator


# def user_management_cli(user_manager):
#     print(f'Welcome to users application\n')
#
#     while True:
#         user_command = input('>>>')
#
#         commands = {
#             'create': user_manager.create,
#             'read': user_manager.read,
#             # 'update': user_manager.update_user,
#             'delete': user_manager.delete,
#         }
#
#         if user_command in commands:
#             func = commands[user_command]
#             func()
#         elif user_command == 'exit':
#             print('Exiting')
#             break
#         else:
#             print('Unsupported command')


if __name__ == "__main__":
    user_manager = UserManager("test.txt")
    validator = Validator()
    input_manager = InputManager(validator, user_manager)

    while True:
        user_command = input('>>>')

        commands = {
            'create': input_manager.create,
            'read': input_manager.read,
            # 'update': user_manager.update_user,
            'delete': input_manager.delete,
        }

        if user_command in commands:
            func = commands[user_command]
            print(func())
        elif user_command == 'exit':
            print('Exiting')
            break
        else:
            print('Unsupported command')
