from interactors.storage_interface.postgres_storage_interface import PostgresStorageInterface


class PopulatePostgresInteractor:
    def __init__(self, storage:PostgresStorageInterface,db,cursor,db_name):
        self.storage = storage
        self.db = db
        self.cursor = cursor
        self.db_name = db_name


    def create_postgres_db_tables(self):
        self.storage.create_db(self.cursor, self.db_name)
        self.storage.create_author_table(self.cursor)
        self.storage.create_quote_table(self.cursor)
        self.storage.create_tag_table(self.cursor)
        self.storage.create_quote_tag_table(self.cursor)

    def populate_postgres_database(self):
        self.create_postgres_db_tables()
        self.storage.insert_authors(self.db, self.cursor)
        self.storage.insert_quotes(self.db, self.cursor)
        self.storage.insert_tags(self.db, self.cursor)
        self.storage.insert_quote_tag(self.db, self.cursor)