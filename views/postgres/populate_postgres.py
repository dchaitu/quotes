import psycopg2

from interactors.populate_postgres_interactor import PopulatePostgresInteractor
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

interactor = PopulatePostgresInteractor(storage=storage,db_name=DB_NAME,db=db,cursor=cursor)
interactor.populate_postgres_database()