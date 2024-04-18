import json
import html2text
from prettytable import PrettyTable
import datetime

from lecture_28.event import Event
from lecture_28.speaker import Speaker
from lecture_28.venue import Venue
from lecture_28.exceptions import (VenueAlreadyExistsError,
                                   SpeakerAlreadyExistsError,
                                   SpeakerDoesNotExistError,
                                   VenueDoesNotExistError,
                                   SpeakerIsUsedInEventError,
                                   EventDoesNotExist,
                                   NoEventFound,
                                   DatesIntervalError)


class Conference:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.speakers: dict[int:Speaker] = {}
        self.venues: dict[int:Venue] = {}
        self.events: dict[int:Event] = {}
        self.__parse_data_from_file()

    @staticmethod
    def _check_json_format(data):
        try:
            json.loads(data)
        except ValueError as error:
            print(error)
            return False
        return True

    def __extract_json_file_data(self):
        with open(self.filepath) as file:
            content = file.read()
            if self._check_json_format(content):
                data = json.loads(content)
        return data

    def __parse_data_from_file(self):
        file_data = self.__extract_json_file_data()["Schedule"]

        for venue in file_data["venues"]:
            self.venues[venue["serial"]] = Venue(
                serial=venue["serial"],
                name=venue["name"],
                category=venue["category"]
            )

        for speaker in file_data["speakers"]:
            self.speakers[speaker["serial"]] = Speaker(
                serial=speaker["serial"],
                name=speaker["name"],
                photo=speaker["photo"],
                url=speaker["url"],
                position=speaker["position"],
                affiliation=speaker["affiliation"],
                twitter=speaker["twitter"],
                bio=html2text.html2text(speaker["bio"])
            )

        for event in file_data["events"]:
            speakers = []
            if event.get("speakers") is not None:
                for speaker in event["speakers"]:
                    if speaker in self.speakers:
                        speakers.append(speaker)

            serial = event.get("serial")
            name = event.get("name").strip()
            event_type = event.get("event_type")
            time_start = event.get("time_start").strip()
            time_stop = event.get("time_stop").strip()
            venue_serial = event.get("venue_serial")
            description = event.get("description")
            website_url = event.get("website_url")
            categories = event.get("categories")

            if event["venue_serial"] not in self.venues:
                raise VenueDoesNotExistError(f"The venue with the serial {event["venue_serial"]} does not exist")

            self.events[event["serial"]] = Event(
                serial=serial,
                name=name,
                event_type=event_type,
                time_start=time_start,
                time_stop=time_stop,
                venue_serial=venue_serial,
                description=description if description else "",
                website_url=website_url,
                speakers=speakers,
                categories=categories
            )

    def _generate_serial_number(self, class_instance: str):
        if class_instance == "speaker":
            max_serial = max(self.speakers)
        elif class_instance == "venue":
            max_serial = max(self.venues)
        elif class_instance == "event":
            max_serial = max(self.events)
        else:
            return None
        return max_serial + 1

    def generate_json_file_with_current_data(self):
        pass

    # ---- SPEAKER related methods -------------------------------------------------------------------------------
    def create_speaker(self, name, photo, url, position, affiliation, twitter, bio):
        serial = self._generate_serial_number("speaker")
        for speaker in self.speakers:
            if speaker.get_twitter() == twitter:
                raise SpeakerAlreadyExistsError("User with the same twitter already exists")
            elif speaker.get_url() == url:
                raise SpeakerAlreadyExistsError("User with the same url already exists")
            else:
                pass

        self.speakers[serial] = Speaker(serial, name, photo, url, position, affiliation, twitter, bio)
        return True

    def delete_speaker(self, speaker_serial):
        if speaker_serial not in self.speakers:
            raise SpeakerDoesNotExistError

        used_in_events = []
        for event in self.events:
            if speaker_serial in event.speakers:
                used_in_events.append(event.get_serial())
        if used_in_events:
            raise SpeakerIsUsedInEventError(
                f"Cannot delete the speaker as they are mentioned in the following events: {used_in_events}"
            )
        del self.speakers[speaker_serial]

    # ---- VENUE related methods ------------------------------------------------------------------------------------
    def create_venue(self, name, category):
        serial = self._generate_serial_number("venue")
        for venue in self.venues:
            if venue.get_name() == name and venue.get_category() == category:
                raise VenueAlreadyExistsError

        self.venues[serial] = Venue(serial, name, category)

    def delete_venue(self, venue_serial: int):
        if venue_serial not in self.venues:
            raise VenueDoesNotExistError

        del self.venues[venue_serial]

    # ---- VENUE related methods ------------------------------------------------------------------------------------
    def create_event(
            self,
            name,
            event_type,
            time_start,
            time_stop,
            venue_serial,
            description,
            website_url,
            speakers,
            categories
    ):
        non_existent_speakers = []
        for speaker in speakers:
            if speaker not in self.speakers:
                non_existent_speakers.append(speaker)
        if non_existent_speakers:
            raise SpeakerDoesNotExistError(
                f"The speakers {" ,".join(non_existent_speakers)} do not exist. "
                f"Use create_speaker method to create a speaker first"
            )
        if venue_serial not in self.venues:
            raise VenueDoesNotExistError(
                f"The venue {venue_serial} does not exist. Use create_venue method to create it first"
            )

        serial = self._generate_serial_number("event")
        self.events[serial] = Event(
            serial=serial,
            name=name,
            event_type=event_type,
            time_start=time_start,
            time_stop=time_stop,
            venue_serial=venue_serial,
            description=description,
            website_url=website_url,
            speakers=speakers,
            categories=categories)

    def delete_event(self, event_serial: int):
        if event_serial not in self.events:
            raise EventDoesNotExist
        del self.events[event_serial]

    def get_events_table(self, events):
        table = PrettyTable()
        table.field_names = [
            "Serial", "Name", "Type", "Start time", "End time", "Venue", "URL", "Speakers", "Categories"
        ]
        table._max_width = {"Serial": 10, "Name": 25, "Type": 15, "Start time": 10, "End time": 10, "Venue": 15,
                            "URL": 20, "Speakers": 15, "Categories": 20}
        sorted_events = self._sort_events_by_start_time(events)
        for event_serial in sorted_events:
            event_obj = self.events[event_serial]
            speakers = []
            if event_obj.speakers:
                for serial in event_obj.speakers:
                    # if not self.speakers.get(serial):
                    #     continue
                    speakers.append(self.speakers[serial].get_name())

            speakers = speakers[0] if len(speakers) == 1 else ", ".join(speakers)

            table.add_row(
                [
                    event_obj.get_serial(),
                    event_obj.get_name(),
                    event_obj.get_event_type(),
                    event_obj.get_time_start(),
                    event_obj.get_time_stop(),
                    self.venues[event_obj.venue_serial].get_name(),
                    event_obj.get_website_url(),
                    speakers,
                    ", ".join(event_obj.get_categories())
                ]
            )
        return table

    def filter_events_by_date(self, date: datetime.datetime):
        filtered = []
        for event in self.events.values():
            if event.get_time_start().date() == date.date() and event.get_time_start().time() >= date.time():
                filtered.append(event.get_serial())
        return filtered

    def filter_by_date_interval(self, from_date: datetime.datetime, till_date: datetime.datetime, till_date_time):
        filtered = []
        if till_date_time and from_date > till_date:
            raise DatesIntervalError("From date is older than till date")

        till_date_next = till_date + datetime.timedelta(1)
        for event in self.events.values():
            if till_date_time:
                if from_date <= event.get_time_start() <= till_date:
                    filtered.append(event.get_serial())
            else:
                if from_date <= event.get_time_start() < till_date_next:
                    filtered.append(event.get_serial())
        if not filtered:
            raise NoEventFound("Such event is not found, double-check the entry data.")
        return filtered

    def filter_events_by_category(self, category: str):
        filtered = []
        for event in self.events.values():
            categories = [category.lower() for category in event.get_categories()]
            if category in categories:
                filtered.append(event.get_serial())
        if not filtered:
            raise NoEventFound(f"Events of category '{category}' not found")
        return filtered

    def filter_event_by_speaker(self, speaker_serial=0, speaker_name=""):
        filtered = []
        speaker = [speaker.get_serial() for speaker in self.speakers.values() if speaker.get_name() == speaker_name]
        for event in self.events.values():
            if speaker_serial in event.get_speakers() or speaker[0] in event.get_speakers():
                filtered.append(event.get_serial())
        return filtered

    def find_event_by_key_word(self, key_word: str):
        found_events = []
        for event in self.events.values():
            if event.contains_key_word(key_word):
                found_events.append(event.get_serial())
        if not found_events:
            raise NoEventFound("Such event is not found, double-check the entry data.")
        return found_events

    def _sort_events_by_start_time(self, events: str | list = ""):
        if not events:
            sorted_events = [
                event.get_serial() for event
                in sorted(self.events.values(), key=lambda value: value.get_time_start())
            ]
        else:
            events_obj = [event for event in self.events.values() if event.get_serial() in events]
            sorted_events = [
                event.get_serial() for event
                in sorted(events_obj, key=lambda value: value.get_time_start())
            ]
        return sorted_events

    def find_event_by_name(self, name: str):
        event = [event.get_serial() for event in self.events.values() if name.lower() == event.get_name().lower()]
        if not event:
            raise EventDoesNotExist(f"Event with name '{name}' does not exist")
        return event

    def find_event_by_serial(self, serial: int):
        if serial not in self.events:
            raise EventDoesNotExist(f"Event with serial number {serial} does not exist")
        return [serial]
