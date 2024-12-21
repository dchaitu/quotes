import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from interactors.populate_sqlite_sqlalchemy_interactor import PopulateSqliteSqlalchemyInteractor
from models.base import Base
from storages.sql_alchemy_storage_implementation import SqlAlchemyStorageImplementation

storage =  SqlAlchemyStorageImplementation()
engine = sa.create_engine('sqlite:///sqlite_sqlalchemy_quotes.db', echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(bind=engine)
interactor = PopulateSqliteSqlalchemyInteractor(storage=storage, session=session)

interactor.populate_database()
