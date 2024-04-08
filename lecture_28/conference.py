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
                                   EventDoesNotExist)


class Conference:

    def __init__(self, filepath: str):
        self.filepath = filepath
        # change to lists
        self.speakers: dict[int:Speaker] = {}
        self.venues: dict[int:Venue] = {}
        self.events: dict[int:Event] = {}
        self._parse_data_from_file()

    @staticmethod
    def _check_json_format(data):
        try:
            json.loads(data)
        except ValueError as error:
            print(error)
            return False
        return True

    def _extract_json_file_data(self):
        with open(self.filepath) as file:
            content = file.read()
            if self._check_json_format(content):
                data = json.loads(content)
        return data

    def _parse_data_from_file(self):
        """
        Parses data from the file stated during the initialization
        Places corresponding classes objects (event, venue, speaker)
        into Conference class attributes as dicts
        :return: None
        """
        file_data = self._extract_json_file_data()["Schedule"]

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
            # speakers = []
            # for speaker in event["speakers"]:
            #     if speaker in self.speakers:
            #         speakers.append(speaker)
            #     else:
            #         raise SpeakerDoesNotExistError(f"The speaker with the serial {speaker} does not exist")

            serial = event.get("serial")
            name = event.get("name")
            event_type = event.get("event_type")
            time_start = event.get("time_start")
            time_stop = event.get("time_stop")
            venue_serial = event.get("venue_serial")
            description = event.get("description")
            website_url = event.get("website_url")
            speakers = event.get("speakers")
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
        """
        Generates the serial number in a sequential order depending on the max serial number
        in the given group of objects: events, venues, speakers
        :param class_instance: type of object - 'event', 'venue', 'speaker'
        :return: serial number (int) | None if the type of object is not among the existing
        """
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
        """
        Creates speaker object and places it into the Conference class dict attribute - speakers
        :return: True if speaker object is created | None if couldn't create an object and errors raised
        """
        serial = self._generate_serial_number("speaker")
        for speaker in self.speakers:
            if speaker.twitter == twitter:
                raise SpeakerAlreadyExistsError("User with the same twitter already exists")
            elif speaker.url == url:
                raise SpeakerAlreadyExistsError("User with the same url already exists")
            else:
                pass

        self.speakers[serial] = Speaker(serial, name, photo, url, position, affiliation, twitter, bio)
        return True

    def view_speakers(self, *speakers):
        table = PrettyTable()
        table.field_names = ["Serial", "Name", "Photo", "URL", "Position", "Affiliation", "Twitter", "Bio"]
        table._max_width = {"Serial": 10, "Name": 15, "Photo": 20, "URL": 20, "Position": 15, "Affiliation": 15,
                            "Twitter": 20, "Bio": 50}
        for speaker in speakers:
            if speaker in self.speakers:
                speaker_obj = self.speakers[speaker]
                table.add_row(
                    [
                        speaker_obj.serial,
                        speaker_obj.name,
                        speaker_obj.photo,
                        speaker_obj.url,
                        speaker_obj.position,
                        speaker_obj.affiliation,
                        speaker_obj.twitter,
                        speaker_obj.bio
                    ]
                )
        return table

    def delete_speaker(self, speaker_serial):
        if speaker_serial not in self.speakers:
            raise SpeakerDoesNotExistError

        used_in_events = []
        for event in self.events:
            if speaker_serial in event.speakers:
                used_in_events.append(event.serial)
        if used_in_events:
            raise SpeakerIsUsedInEventError(
                f"Cannot delete the speaker as they are mentioned in the following events: {", ".join(used_in_events)}"
            )
        del self.speakers[speaker_serial]
        return True

    # ---- VENUE related methods ------------------------------------------------------------------------------------
    def create_venue(self, name, category):
        serial = self._generate_serial_number("venue")
        for venue in self.venues:
            if venue.name == name and venue.category == category:
                raise VenueAlreadyExistsError

        self.venues[serial] = Venue(serial, name, category)
        return True

    def delete_venue(self, venue_serial: int):
        if venue_serial not in self.venues:
            raise VenueDoesNotExistError

        del self.venues[venue_serial]
        return True

    # def view_venue(self, *venues):
    #     if venue_serial in self.venues:
    #         return self.venues[venue_serial]


    #  EVENT related methods
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
            raise SpeakerAlreadyExistsError(
                f"The speakers {" ,".join(non_existent_speakers)} do not exist. Use create_speaker method first"
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
        return True

    def view_events(self, events):
        table = PrettyTable()
        table.field_names = ["Serial", "Name", "Type", "Start time", "End time", "Venue", "URL", "Speakers", "Categories"]
        table._max_width = {"Serial": 10, "Name": 30, "Type": 15, "Start time": 10, "End time": 10, "Venue": 15,
                            "URL": 20, "Speakers": 15, "Categories": 20}
        for event_serial in events:
            if event_serial in self.events:
                event_obj = self.events[event_serial]
                speakers = []
                for serial in event_obj.speakers:
                    speakers.append(self.speakers[serial].name)

                table.add_row(
                    [
                        event_obj.serial,
                        event_obj.name,
                        event_obj.event_type,
                        event_obj.time_start,
                        event_obj.time_stop,
                        self.venues[event_obj.venue_serial].name,
                        event_obj.website_url,
                        speakers,
                        ", ".join(event_obj.categories)
                    ]
                )
        return table

    def filter_events_by_date(self, start_date: str, end_date: str):
        start_date = datetime.datetime.fromisoformat(start_date)
        end_date = datetime.datetime.fromisoformat(end_date)
        filtered = []
        for event in self.events.values():
            if event.time_start >= start_date and event.time_stop <= end_date:
                filtered.append(event.serial)
        return filtered

    def filter_events_by_category(self, category: str):
        filtered = []
        for event in self.events.values():
            if category in event.categories:
                filtered.append(event.serial)
        return filtered

    def filter_event_by_speaker(self, speaker_serial=0, speaker_name=""):
        filtered = []
        speaker = [speaker.serial for speaker in self.speakers.values() if speaker.name == speaker_name]
        for event in self.events.values():
            if speaker_serial in event.speakers or speaker[0] in event.speakers:
                filtered.append(event.serial)
        return filtered

    def find_event_by_key_word(self, key_word: str):
        found_events = []
        for event in self.events.values():
            if event.contains_key_word(key_word):
                found_events.append(event.serial)
        return found_events


if __name__ == "__main__":
    folder = "lecture_28"
    file_name = "py_fest.json"
    conference = Conference(file_name)
    filtered_ev = conference.filter_events_by_date("2014-07-22", "2014-07-23")
    print(conference.view_events(filtered_ev))
