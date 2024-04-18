import datetime


class Event:

    def __init__(
            self,
            serial,
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
        self.serial = serial
        self.name = name
        self.type = event_type
        self.time_start = datetime.datetime.fromisoformat(time_start)
        self.time_stop = datetime.datetime.fromisoformat(time_stop)
        self.venue_serial = venue_serial
        self.description = description
        self.website_url = website_url
        self.speakers = speakers
        self.categories = categories

    def __repr__(self):
        return f"Event serial: {self.serial}, name: {self.name}. start: {self.time_start}"

    def __str__(self):
        return f"""
        Event serial: {self.serial}
        Name: {self.name}
        Type: {self.type}
        Start: {self.time_start}
        End: {self.time_stop}
        Description: {self.description}
        Url: {self.website_url}
        Speakers: {self.speakers}
        Categories: {self.categories}
        """

    def get_serial(self):
        return self.serial

    def get_name(self):
        return self.name

    def update_name(self, name):
        self.name = name

    def get_event_type(self):
        return self.type

    def update_event_type(self, new_type):
        self.type = new_type

    def get_time_start(self):
        return self.time_start

    def update_time_start(self, time_start):
        try:
            self.time_start = datetime.datetime.fromisoformat(time_start)
        except ValueError as error:
            print(error)

    def get_time_stop(self):
        return self.time_stop

    def update_time_stop(self, time_stop):
        try:
            self.time_start = datetime.datetime.fromisoformat(time_stop)
        except ValueError as error:
            print(error)

    def get_venue_serial(self):
        return self.venue_serial

    def update_venue_serial(self, venue_serial: str):
        if venue_serial.isnumeric():
            self.venue_serial = int(venue_serial)
        else:
            raise ValueError("Non-numeric serial number")

    def get_description(self):
        return self.description

    def update_description(self, description):
        self.description = description

    def get_website_url(self):
        return self.website_url

    def update_website_url(self, website_url):
        self.website_url = website_url

    def get_speakers(self):
        return self.speakers

    def update_speakers(self, speakers: list[int]):
        self.speakers = speakers

    def get_categories(self):
        return self.categories

    def update_categories(self, categories: list[str]):
        self.categories = categories

    def get_all(self):
        return {
            "serial": self.serial,
            "name": self.name,
            "type": self.type,
            "time_start": self.time_start,
            "time_stop": self.time_stop,
            "venue_serial": self.venue_serial,
            "description": self.description,
            "website_url": self.website_url,
            "speakers": self.speakers,
            "categories": self.categories
        }

    def contains_key_word(self, key_word):
        if key_word in self.name.lower() or key_word in self.description.lower():
            return True
        return False
