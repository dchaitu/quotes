import sqlite3

from interactors.populate_sqlite_interactor import PopulateSQliteInteractor
from storages.sqlite_storage_implementation import SqliteStorageImplementation

db_name = 'sqlite_quotes.db'

with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    storage = SqliteStorageImplementation()
    interactor = PopulateSQliteInteractor(storage=storage, cursor=cursor)
    interactor.populate_sqlite()
