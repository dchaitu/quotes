from interactors.storage_interface.storage_interface import SqlAlchemyStorageInterface


class QuerySqliteDatabaseSqlalchemyInteractor:
    def __init__(self, storage: SqlAlchemyStorageInterface, session):
        self.storage = storage
        self.session = session


    def get_quote(self, quote_id: int):
        result = self.storage.get_quote(self.session,quote_id)
        return result

    def get_quotes_by_author(self, author_name:str):
        quote_list = self.storage.get_quotes_by_author(self.session,author_name)
        return quote_list

    def get_quotes_by_tag(self, tag: str):
        quote_list = self.storage.get_quotes_by_tag(self.session,tag)
        return quote_list

    def get_quotes_by_search_text(self, search_text: str):
        quote_list = self.storage.get_quotes_by_search_text(self.session,search_text)
        return quote_list
