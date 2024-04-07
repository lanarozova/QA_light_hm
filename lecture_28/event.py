#   Розробіть клас Event, який представлятиме окрему подію з вашого JSON-файлу.
#   Клас повинен включати атрибути для зберігання даних про подію
#   (наприклад, serial, name, event_type, time_start, time_stop,
#   venue_serial, description, website_url, speakers, categories)
#   і методи для роботи з цими даними.

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
        self.event_type = event_type
        self.time_start = time_start
        self.time_stop = time_stop
        self.venue_serial = venue_serial
        self.description = description
        self.website_url = website_url
        self.speakers = speakers
        self.categories = categories
