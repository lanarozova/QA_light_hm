#   Розробіть клас Event, який представлятиме окрему подію з вашого JSON-файлу.
#   Клас повинен включати атрибути для зберігання даних про подію
#   (наприклад, serial, name, event_type, time_start, time_stop,
#   venue_serial, description, website_url, speakers, categories)
#   і методи для роботи з цими даними.
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
        return f"Event serial: {self.serial}, name: {self.name}"

    def __str__(self):
        speakers = [speaker.name for speaker in self.speakers]
        return f"""
        Event serial: {self.serial}
        Name: {self.name}
        Type: {self.event_type}
        Start: {self.time_start}
        End: {self.time_stop}
        Description: {self.description}
        Url: {self.website_url}
        Speakers: {", ".join(speakers)}
        Categories: {self.categories}
        """

    def get_serial(self):
        return self.serial

    def get_name(self):
        return self.name

    def get_event_type(self):
        return self.type

    def get_time_start(self):
        return self.time_start

    def get_time_stop(self):
        return self.time_stop

    def get_venue_serial(self):
        return self.venue_serial

    def get_description(self):
        return self.description

    def get_website_url(self):
        return self.website_url

    def get_speakers(self):
        return self.speakers

    def get_categories(self):
        return self.categories

    def contains_key_word(self, key_word):
        if key_word in self.name or key_word in self.description:
            return True
        return False
