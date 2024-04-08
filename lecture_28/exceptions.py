class VenueAlreadyExistsError(Exception):
    pass


class VenueDoesNotExistError(Exception):
    pass


class SpeakerAlreadyExistsError(Exception):
    pass


class SpeakerDoesNotExistError(Exception):
    pass


class SpeakerIsUsedInEventError(Exception):
    pass


class EventDoesNotExist(Exception):
    pass
