from interactors.storage_interface.storage_interface import SqlAlchemyStorageInterface


class PopulateSqliteSqlalchemyInteractor:
    def __init__(self, storage: SqlAlchemyStorageInterface, session):
        self.storage = storage
        self.session = session


    def populate_database(self):
        self.storage.insert_authors(self.session)
        self.storage.insert_quotes(self.session)
        self.storage.insert_tags(self.session)
        self.storage.insert_quote_tag(self.session)

