class Venue:

    def __init__(self, serial, name, category):
        self.serial = serial
        self.name = name
        self.category = category

    def __repr__(self):
        return f"Venue serial: {self.serial}, name: {self.name}, category: {self.category}"

    def __str__(self):
        return f"""
        Venue name: {self.name}
        Venue category: {self.category}
        """

    def get_serial(self):
        return self.serial

    def get_name(self):
        return self.name

    def update_name(self, name):
        self.name = name

    def get_category(self):
        return self.category

    def update_category(self, category):
        self.category = category

    def get_all(self):
        return {"serial": self.serial, "name": self.name, "category": self.category}
