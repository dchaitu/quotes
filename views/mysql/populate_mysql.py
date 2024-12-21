import mysql.connector

from interactors.populate_mysql_interactor import PopulateMysqlInteractor
from storages.mysql_storage_implementation import MySqlStorageImplementation

USER = "root"
PASSWORD = "password"
DB_NAME = "mysql_quotes"
HOST = "172.24.0.2"

with mysql.connector.connect(host=HOST, user=USER, password=PASSWORD) as db:
    storage = MySqlStorageImplementation()
    cursor = db.cursor()

    interactor = PopulateMysqlInteractor(storage=storage,db_name=DB_NAME,db=db,cursor=cursor)
    interactor.populate_database()