import abc


class SqlAlchemyStorageInterface(abc.ABC):
    @abc.abstractmethod
    def get_author_id(self, session, author_name):
        pass

    @abc.abstractmethod
    def get_quote(self, session, quote_id):
        pass

    @abc.abstractmethod
    def get_quotes_by_author(self, session, author_name):
        pass

    @abc.abstractmethod
    def get_quotes_by_tag(self, session, tag):
        pass

    @abc.abstractmethod
    def get_quotes_by_search_text(self, session, search_text):
        pass

    @abc.abstractmethod
    def insert_quote_tag(self, session):
        pass

    @abc.abstractmethod
    def insert_tags(self, session):
        pass


    @abc.abstractmethod
    def insert_quotes(self, session):
        pass


    @abc.abstractmethod
    def insert_authors(self, session):
        pass
