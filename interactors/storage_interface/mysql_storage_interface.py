import abc


class MySqlStorageInterface(abc.ABC):
    def create_db(self, cursor, db_name):
        pass

    def create_quote_table(self, cursor):
        pass

    def create_tag_table(self, cursor):
        pass

    def create_quote_tag_table(self, cursor):
        pass

    def create_author_table(self, cursor):
        pass

    def insert_authors(self, db, cursor):
        pass

    def insert_quotes(self, db, cursor):
        pass

    def insert_tags(self, db, cursor):
        pass

    def insert_quote_tag(self, db, cursor):
        pass

    def get_author_id(self, cursor, name):
        pass

    def get_quote(self, cursor, quote_id):
        pass

    def get_quotes_by_author(self, cursor, author_name):
        pass

    def get_quotes_by_tag(self, cursor, tag):
        pass

    def get_quotes_by_search_text(self, cursor, search_text):
        pass