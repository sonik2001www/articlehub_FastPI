class AuthError(Exception):
    """Basic error for auth domain."""


class ConflictError(AuthError):
    """For example, email already exists."""


class UnauthorizedError(AuthError):
    """Invalid credentials / no access."""
