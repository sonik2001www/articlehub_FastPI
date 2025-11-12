from tests.fixtures.users import TEST_USER_EMAIL, TEST_USER_NAME

pytest_plugins = [
    "tests.fixtures.db",
    "tests.fixtures.client",
    "tests.fixtures.users",
    "tests.fixtures.articles",
    "tests.fixtures.auth",
]
