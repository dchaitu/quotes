from interactors.storage_interface.sqlite_storage_interface import SqliteStorageInterface


class PopulateSQliteInteractor:
    def __init__(self, storage: SqliteStorageInterface,cursor):
        self.storage = storage
        self.cursor = cursor


    def create_tables(self):
        self.storage.create_author_table(self.cursor)
        self.storage.create_quote_table(self.cursor)
        self.storage.create_tag_table(self.cursor)
        self.storage.create_quote_tag_table(self.cursor)


    def populate_sqlite(self):
        self.create_tables()
        self.storage.insert_authors(self.cursor)
        self.storage.insert_quotes(self.cursor)
        self.storage.insert_tags(self.cursor)
        self.storage.insert_quote_tag(self.cursor)

