import sys

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from interactors.query_sqlite_database_sqlalchemy_interactor import QuerySqliteDatabaseSqlalchemyInteractor
from models.base import Base
from storages.sql_alchemy_storage_implementation import SqlAlchemyStorageImplementation

USER = "root"
PASSWORD = "password"
DB_NAME = "quotes"
HOST = "172.24.0.1"
PORT_ID = 3333


storage =  SqlAlchemyStorageImplementation()


def setup_tables():
    # Connect to the default 'mysql' database
    engine = sa.create_engine(
        f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT_ID}",
        echo=True,
    )
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        result = conn.execute(sa.text(f"SHOW DATABASES LIKE '{DB_NAME}';")).fetchone()
        if not result:
            conn.execute(sa.text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
            conn.execute(sa.text(f"USE {DB_NAME};"))
        else:
            print(f"Database '{DB_NAME}' already exists.")

    engine = sa.create_engine(
        f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT_ID}/{DB_NAME}",
        echo=True,
    )

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = setup_tables()
interactor = QuerySqliteDatabaseSqlalchemyInteractor(storage=storage,session=session)


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