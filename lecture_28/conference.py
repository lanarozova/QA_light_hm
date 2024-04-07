import json
from event import Event
from lecture_28.speaker import Speaker
from lecture_28.venue import Venue


class Conference:

    def __init__(self, filepath):
        self.filepath = filepath
        self.speakers = {}
        self.venues = {}
        self.events = {}

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

    def _create_class_attributes(self):
        file_data = self._extract_json_file_data()

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
                bio=speaker["bio"],
            )

        for event in file_data["events"]:

            speakers = [self.speakers[speaker] for speaker in event["speakers"] if speaker in self.speakers]
            venue = self.venues[event["venues"]]

            self.events[event["serial"]] = Event(
                            serial=event["serial"],
                            name=event["name"],
                            event_type=event["event_type"],
                            time_start=event["time_start"],
                            time_stop=event["time_stop"],
                            venue_serial=venue,
                            description=event["description"],
                            website_url=event["website_url"],
                            speakers=speakers,
                            categories=event["categories"]
                        )



