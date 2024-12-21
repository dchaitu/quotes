import sys

import psycopg2

from interactors.query_postgres_interactor import QueryPostgresInteractor
from storages.postgres_storage_implementation import PostgresStorageImplementation

USER = "chaitu"
PASSWORD = "pwd"
DB_NAME = "postgres_quotes"
HOST = "localhost"
PORT_ID = 4444

def connect_to_postgres_db(host, user, password, port, dbname):
    """Connect to a PostgreSQL database and return the connection."""
    try:
        return psycopg2.connect(
            host=host, dbname=dbname, user=user, password=password, port=port
        )
    except psycopg2.Error as e:
        print(f"Failed to connect to {dbname}: {e}")
        return None

post_conn = connect_to_postgres_db(HOST, USER, PASSWORD, PORT_ID, "postgres")
if not post_conn:
    pass
post_conn.autocommit = True
cursor = post_conn.cursor()

storage = PostgresStorageImplementation()


if not storage.database_exists(cursor, DB_NAME):
    storage.create_db(cursor, DB_NAME)
else:
    print(f"Database '{DB_NAME}' already exists.")
    cursor.close()
    post_conn.close()


db = psycopg2.connect(host=HOST, user=USER, password=PASSWORD)
cursor = db.cursor()

interactor = QueryPostgresInteractor(storage=storage, cursor=cursor)
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