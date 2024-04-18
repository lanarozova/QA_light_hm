import datetime

from lecture_28.conference import Conference
from prettytable import PrettyTable


class InputManager:

    def __init__(self,  conference: Conference):
        self.conference = conference

    def find_by_event_serial_name(self) -> PrettyTable:
        inp = input("Enter an event name or serial number: ").strip()
        if inp.isdigit():
            events = self.conference.find_event_by_serial(int(inp))
        else:
            events = self.conference.find_event_by_name(inp)
        return self.conference.get_events_table(events)

    def find_by_key_word(self) -> PrettyTable:
        key_word = input("Enter a kew word to find events: ").strip().lower()
        events = self.conference.find_event_by_key_word(key_word)
        return self.conference.get_events_table(events)

    def find_events_by_date(self):
        print("Acceptable datetime format: 'YYYY-MM-DD HH:MM:SS'")
        from_date = datetime.datetime.fromisoformat(input("Enter a 'from' date or date and time: ").strip())
        till_date_str = input("Enter a 'till' date or date and time. If need events for a single date, skip: ").strip()
        if not till_date_str:
            events = self.conference.filter_events_by_date(from_date)
        else:
            time_flag = True
            try:
                datetime.date.fromisoformat(till_date_str)
                time_flag = False
            except ValueError:
                pass
            till_date = datetime.datetime.fromisoformat(till_date_str)
            events = self.conference.filter_by_date_interval(from_date, till_date, time_flag)
        return self.conference.get_events_table(events)

    def find_events_by_category(self):
        category = input("Enter the category of needed events: ").strip().lower()
        events = self.conference.filter_events_by_category(category)
        return self.conference.get_events_table(events)
