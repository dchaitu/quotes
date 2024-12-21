from interactors.storage_interface.sqlite_storage_interface import SqliteStorageInterface


class QuerySqliteInteractor:
    def __init__(self, storage: SqliteStorageInterface, cursor):
        self.storage = storage
        self.cursor = cursor


    def get_author_id(self, name:str):
        return self.storage.get_author_id(self.cursor, name)

    def get_quote(self, quote_id: int):
        return self.storage.get_quote(self.cursor, quote_id)

    def get_quotes_by_author(self, author_name: str):
        quotes = self.storage.get_quotes_by_author(self.cursor, author_name)
        return [quote[0] for quote in quotes]

    def get_quotes_by_tag(self, tag: str):
        quotes = self.storage.get_quotes_by_tag(self.cursor, tag)
        return [quote[0] for quote in quotes]


    def get_quotes_by_search_text(self, search_text: str):
        quotes = self.storage.get_quotes_by_search_text(self.cursor, search_text)
        return [quote[0] for quote in quotes]
