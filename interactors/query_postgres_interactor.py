from interactors.storage_interface.postgres_storage_interface import PostgresStorageInterface


class QueryPostgresInteractor:

    def __init__(self,storage: PostgresStorageInterface,cursor):
        self.storage = storage
        self.cursor = cursor


    def get_author_id(self,name:str):
        return self.storage.get_author_id(self.cursor,name)

    def get_quote(self, quote_id: int):
        return self.storage.get_quote(self.cursor,quote_id)

    def get_quotes_by_author(self, author_name: str):
        return self.storage.get_quotes_by_author(self.cursor,author_name)

    def get_quotes_by_tag(self, tag: str):
        return self.storage.get_quotes_by_tag(self.cursor,tag)

    def get_quotes_by_search_text(self, search_text: str):
        return self.storage.get_quotes_by_search_text(self.cursor,search_text)

    
