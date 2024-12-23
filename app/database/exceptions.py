class DatabaseException(Exception):
    pass


class EntryNotFoundError(DatabaseException):
    pass
