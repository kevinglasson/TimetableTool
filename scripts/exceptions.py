# Trying to implement custom error messages... will work on this


class LoginFailedError(Exception):
    """Store the html response code on login exception."""

    def __init__(self, response):
        """Store the respose code in instance variable."""
        self.response = response


class NavigationFailedError(Exception):
    """Store the html response code on login exception."""

    def __init__(self, response):
        """Store the respose code in instance variable."""
        self.response = response
