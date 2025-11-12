import pytest

from app.models import ARTICLES_COL


@pytest.fixture
def test_articles(mongo_db, test_user):
    """Insert a few example articles for tests that need existing data."""
    articles_col = mongo_db[ARTICLES_COL]

    sample_articles = [
        {
            "title": "First article",
            "content": "Lorem ipsum",
            "author_email": test_user["email"],
        },
        {
            "title": "Second article",
            "content": "Dolor sit amet",
            "author_email": test_user["email"],
        },
    ]

    articles_col.insert_many(sample_articles)
    return sample_articles
