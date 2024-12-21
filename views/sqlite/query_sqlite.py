import sqlite3
import sys

from interactors.query_sqlite_interactor import QuerySqliteInteractor
from storages.sqlite_storage_implementation import SqliteStorageImplementation

db_name = 'sqlite_quotes.db'

with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    storage = SqliteStorageImplementation()
    interactor = QuerySqliteInteractor(storage=storage, cursor=cursor)

if __name__ == '__main__':
    if sys.argv[1] == "--quote" or sys.argv[1] == "-q":
        quote_id = int(sys.argv[2])
        quote = interactor.get_quote(quote_id)
        print(quote)

    elif sys.argv[1] == "--author" or sys.argv[1] == "-a":
        author_name = sys.argv[2]
        author_quotes = interactor.get_quotes_by_author(author_name)
        print(author_quotes)

    elif sys.argv[1] == "--tag" or sys.argv[1] == "-t":
        tag = sys.argv[2]
        author_quotes = interactor.get_quotes_by_tag(tag)
        print(author_quotes)

    elif sys.argv[1] == "--search" or sys.argv[1] == "-s":
        search_text = sys.argv[2]
        author_quotes = interactor.get_quotes_by_search_text(search_text)
        print(author_quotes)