from interactors.storage_interface.mysql_storage_interface import MySqlStorageInterface


class QueryMySQLInteractor:
    def __init__(self, storage:MySqlStorageInterface,db,cursor,db_name):
        self.storage = storage
        self.db = db
        self.cursor = cursor
        self.db_name = db_name


    def get_author_id(self,name:str):
        author_id = self.storage.get_author_id(self.cursor, name)
        return author_id


    def get_quote(self, quote_id: int):
        quote = self.storage.get_quote(self.cursor, quote_id)[0]
        return quote

    def get_quotes_by_author(self, author_name: str):
        quotes = self.storage.get_quotes_by_author(self.cursor, author_name)
        return [quote[0] for quote in quotes]

    def get_quotes_by_tag(self, tag: str):
        quotes = self.storage.get_quotes_by_tag(self.cursor, tag)
        return [quote[0] for quote in quotes]

    def get_quotes_by_search_text(self, search_text:str):
        quotes = self.storage.get_quotes_by_search_text(self.cursor, search_text)
        return [quote[0] for quote in quotes]