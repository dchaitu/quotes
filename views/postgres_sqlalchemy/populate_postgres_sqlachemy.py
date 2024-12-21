import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from interactors.populate_sqlite_sqlalchemy_interactor import PopulateSqliteSqlalchemyInteractor
from models.base import Base
from storages.sql_alchemy_storage_implementation import SqlAlchemyStorageImplementation


USER = "chaitu"
PASSWORD = "pwd"
DB_NAME = "postgres_quotes_sqlalchemy"
HOST = "localhost"
PORT_ID = 4445



def create_database():
    try:
        # Connect to the default 'postgres' database
        engine = sa.create_engine(
            f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT_ID}/postgres",
            echo=True
        )
        with engine.connect() as conn:
            # conn.autocommit = True
            conn.execution_options(isolation_level="AUTOCOMMIT")
            result = conn.execute(
                sa.text(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
            ).fetchone()

            if not result:
                conn.execute(sa.text(f"CREATE DATABASE {DB_NAME}"))
                print(f"Database '{DB_NAME}' created successfully!")
            else:
                print(f"Database '{DB_NAME}' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")


def setup_tables():
    engine = sa.create_engine(
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT_ID}/{DB_NAME}", echo=True
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

create_database()
session = setup_tables()
storage = SqlAlchemyStorageImplementation()
interactor = PopulateSqliteSqlalchemyInteractor(storage=storage, session=session)

interactor.populate_database()


