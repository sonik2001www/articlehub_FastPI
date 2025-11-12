# tests/fixtures/async_db.py

class AsyncCursor:
    """
    Minimal Motor-like async cursor over a mongomock cursor.
    Supports sort(), skip(), limit() and `async for` / await to_list().
    """

    def __init__(self, cursor):
        self._cursor = cursor
        self._iter = None

    def sort(self, *args, **kwargs):
        self._cursor = self._cursor.sort(*args, **kwargs)
        return self

    def skip(self, *args, **kwargs):
        self._cursor = self._cursor.skip(*args, **kwargs)
        return self

    def limit(self, *args, **kwargs):
        self._cursor = self._cursor.limit(*args, **kwargs)
        return self

    async def to_list(self, length=None):
        result = []
        for doc in self._cursor:
            result.append(doc)
            if length is not None and len(result) >= length:
                break
        return result

    def __aiter__(self):
        self._iter = iter(self._cursor)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration


class AsyncCollection:
    """Async-style wrapper around a mongomock collection."""

    def __init__(self, coll):
        self._coll = coll

    # базові async-методи
    async def find_one(self, *args, **kwargs):
        return self._coll.find_one(*args, **kwargs)

    async def insert_one(self, *args, **kwargs):
        return self._coll.insert_one(*args, **kwargs)

    async def insert_many(self, *args, **kwargs):
        return self._coll.insert_many(*args, **kwargs)

    async def delete_many(self, *args, **kwargs):
        return self._coll.delete_many(*args, **kwargs)

    async def delete_one(self, *args, **kwargs):
        return self._coll.delete_one(*args, **kwargs)

    async def update_one(self, *args, **kwargs):
        return self._coll.update_one(*args, **kwargs)

    async def count_documents(self, *args, **kwargs):
        """Motor-style count_documents wrapper."""
        return self._coll.count_documents(*args, **kwargs)

    # find НЕ async: повертає курсор
    def find(self, *args, **kwargs):
        return AsyncCursor(self._coll.find(*args, **kwargs))


class AsyncDB:
    """Async-style DB object that returns AsyncCollection by name."""

    def __init__(self, db):
        self._db = db

    def __getitem__(self, name: str) -> AsyncCollection:
        return AsyncCollection(self._db[name])


