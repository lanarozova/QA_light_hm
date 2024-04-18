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

    def update_name(self, name: str):
        self.name = name

    def get_photo(self):
        return self.photo

    def update_photo(self, photo: str):
        self.photo = photo

    def get_url(self):
        return self.url

    def update_url(self, url: str):
        self.url = url

    def get_position(self):
        return self.position

    def update_position(self, position: str):
        self.position = position

    def get_affiliation(self):
        return self.affiliation

    def update_affiliation(self, affiliation):
        self.affiliation = affiliation

    def get_twitter(self):
        return self.twitter

    def update_twitter(self, twitter: str):
        self.twitter = twitter

    def get_bio(self):
        return self.bio

    def update_bio(self, bio: str):
        self.bio = bio

    def get_all(self):
        return {
            "serial": self.serial,
            "name": self.name,
            "photo": self.photo,
            "url": self.url,
            "position": self.position,
            "affiliation": self.affiliation,
            "twitter": self.twitter,
            "bio": self.bio
        }
