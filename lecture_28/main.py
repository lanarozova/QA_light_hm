from lecture_28.conference import Conference
from lecture_28.input_manager import InputManager
from lecture_28.exceptions import (VenueAlreadyExistsError,
                                   SpeakerAlreadyExistsError,
                                   SpeakerDoesNotExistError,
                                   VenueDoesNotExistError,
                                   SpeakerIsUsedInEventError,
                                   EventDoesNotExist,
                                   NoEventFound,
                                   DatesIntervalError)


def conf_manager(filepath):
    conference = Conference(filepath)
    inp_manager = InputManager(conference)

    commands = {
        "1": inp_manager.find_by_event_serial_name,
        "2": inp_manager.find_by_key_word,
        "3": inp_manager.find_events_by_date,
        "4": inp_manager.find_events_by_category,
    }

    descriptions = {
        "1": "Search by serial number or name",
        "2": "Search by key word in name or description",
        "3": "Search by start date: a single date or within two dates interval",
        "4": "Search by category"
    }

    while True:
        try:
            print("Enter the command: ")
            print("\n".join([f"{k}: {v}" for k, v in descriptions.items()]))

            user_command = input('>>>').strip().lower()

            if user_command in commands:
                func = commands[user_command]
                print(func())
            elif user_command == 'exit':
                break
            else:
                print('Unsupported command')
        except (
            VenueAlreadyExistsError,
            SpeakerAlreadyExistsError,
            SpeakerDoesNotExistError,
            VenueDoesNotExistError,
            SpeakerIsUsedInEventError,
            EventDoesNotExist,
            NoEventFound,
            ValueError,
            DatesIntervalError
        ) as error:
            print(error)


if __name__ == "__main__":
    conf_manager("py_fest.json")
