class EmailValidationError(Exception):
    """Exception raised for errors in the input email.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Email should be of the following format: example@example.com"):
        self.message = message
        super().__init__(self.message)


class NameValidationError(Exception):
    """Exception raised for errors in the input name.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Name should contain only latin letters and a hyphen"):
        self.message = message
        super().__init__(self.message)


class PhoneValidationError(Exception):
    """Exception raised for errors in the input name.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Phone should start with Ukraine country code - 38 and contain 11 digits in total"):
        self.message = message
        super().__init__(self.message)


class UserDoesNotExistError(Exception):
    """Exception raised for errors if the user is not found in the given file.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message="Such user does not exist. Double check the entry data."):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsError(Exception):
    """Exception raised for errors if the user is not found in the given file.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message="Such user already exists."):
        self.message = message
        super().__init__(self.message)


class UpdateInfoNotUniqueError(Exception):
    """Exception raised for errors if the user is not found in the given file.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message="Provided data is not unique. "
                                          "Another user in the file already has the same information."):
        self.message = message
        super().__init__(self.message)


class FieldDoesNotExistError(Exception):
    """Exception raised for errors if the user field does not exist.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message="The provided field does not exist in the file"):
        self.message = message
        super().__init__(self.message)
