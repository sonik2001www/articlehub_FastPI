class UserError(Exception):
    """Basic error for the users domain."""


class UserNotFoundError(UserError):
    """User not found."""
