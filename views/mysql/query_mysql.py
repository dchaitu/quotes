import mysql.connector
import sys
from interactors.query_mysql_interactor import QueryMySQLInteractor
from storages.mysql_storage_implementation import MySqlStorageImplementation

USER = "root"
PASSWORD = "password"
DB_NAME = "mysql_quotes"
HOST = "172.24.0.2"

storage = MySqlStorageImplementation()
db = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
cursor = db.cursor()

interactor = QueryMySQLInteractor(storage=storage,db_name=DB_NAME,db=db,cursor=cursor)
storage.create_db(cursor, DB_NAME)

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
