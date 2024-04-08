class Speaker:

    def __init__(self, serial, name, photo, url, position, affiliation, twitter, bio):
        self.serial = serial
        self.name = name
        self.photo = photo
        self.url = url
        self.position = position
        self.affiliation = affiliation
        self.twitter = twitter
        self.bio = bio

    def __repr__(self):
        return f"Speaker serial: {self.serial}, name: {self.name}, url: {self.url}"

    def __str__(self):
        return (
            f"""
            Speaker name: {self.name}
            Position: {self.position}
            Bio: {self.bio}
            Social:
                twitter: {self.twitter}
            """
        )

    def get_serial(self):
        return self.serial

    def get_name(self):
        return self.name

    def get_photo(self):
        return self.photo

    def get_url(self):
        return self.url

    def get_position(self):
        return self.position

    def get_affiliation(self):
        return self.affiliation

    def get_twitter(self):
        return self.twitter

    def get_bio(self):
        return self.bio


