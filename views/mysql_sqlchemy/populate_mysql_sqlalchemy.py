import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from interactors.populate_sqlite_sqlalchemy_interactor import PopulateSqliteSqlalchemyInteractor
from models.base import Base
from storages.sql_alchemy_storage_implementation import SqlAlchemyStorageImplementation

USER = "root"
PASSWORD = "password"
DB_NAME = "quotes"
HOST = "172.24.0.1"
PORT_ID = 3333



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
storage = SqlAlchemyStorageImplementation()
interactor = PopulateSqliteSqlalchemyInteractor(storage=storage, session=session)

interactor.populate_database()