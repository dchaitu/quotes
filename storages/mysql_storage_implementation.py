import json

from interactors.storage_interface.mysql_storage_interface import MySqlStorageInterface


class MySqlStorageImplementation(MySqlStorageInterface):
    def create_db(self, cursor, db_name):
        DB_NAME = db_name
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

    def create_quote_table(self, cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Quote 
    		(
    		quote_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    		content VARCHAR(500),
    		author_id INTEGER,
    		FOREIGN KEY (author_id) REFERENCES Author(author_id)

    		)"""
        )
        print("Quote Table created")

    def create_tag_table(self, cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Tag 
    		(
    		tag_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    		content VARCHAR(100) NOT NULL UNIQUE
    		)"""
        )
        print("Tag Table created")

    # Through table
    def create_quote_tag_table(self, cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Quote_Tag 
    		(
    		tag_id INTEGER ,
    		quote_id INTEGER,
    		PRIMARY KEY (tag_id, quote_id),
    		FOREIGN KEY (tag_id) REFERENCES Tag(tag_id),
    		FOREIGN KEY (quote_id) REFERENCES Quote(quote_id)
    		)"""
        )

    def create_author_table(self, cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Author
    		(
    		author_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    		name VARCHAR(50) NOT NULL , 
    		born VARCHAR(100) NOT NULL , 
    		reference VARCHAR(150) UNIQUE NOT NULL
    		)"""
        )

    def insert_authors(self, db, cursor):
        with open("./updated_quotes.json", "r") as f:
            json_data = json.load(f)
            author_objs = []
            for author in json_data["authors"]:
                if author["name"] not in author_objs:
                    cursor.execute(
                        """INSERT IGNORE INTO Author (name, born, reference) VALUES (%s, %s, %s)""",
                        (author["name"], author["born"], author["reference"]),
                    )
                author_objs.append(author["name"])
        db.commit()

    def insert_quotes(self, db, cursor):
        with open("./updated_quotes.json", "r") as f:
            json_data = json.load(f)
            quote_objs = []
            for quote in json_data["quotes"]:
                try:
                    author_id = self.get_author_id(cursor, quote["author"])
                    if not author_id:
                        raise ValueError(
                            f"Author ID not found for author: {quote['author']}"
                        )
                    if quote not in quote_objs:
                        cursor.execute(
                            """INSERT IGNORE INTO Quote (quote_id, content, author_id) VALUES (%s, %s, %s)""",
                            (quote["id"], quote["quote"], author_id),
                        )
                except Exception as e:
                    db.rollback()
                    print(f"Error:- {e}")
                else:
                    db.commit()
                quote_objs.append(quote)

    def insert_tags(self, db, cursor):
        with open("./updated_quotes.json", "r") as f:
            json_data = json.load(f)
            for quote in json_data["quotes"]:
                tags = quote["tags"]
                for tag in tags:
                    try:
                        cursor.execute(
                            """INSERT IGNORE INTO Tag (content) VALUES (%s)""", (tag,)
                        )
                    except Exception as e:
                        print(f"{tag}, {e} skipped already present")
        db.commit()

    def insert_quote_tag(self, db, cursor):
        with open("./updated_quotes.json", "r") as f:
            json_data = json.load(f)
            for quote in json_data["quotes"]:
                quote_id = quote["id"]
                tags = quote["tags"]
                for tag in tags:
                    cursor.execute("""SELECT * FROM Tag WHERE content = %s""", (tag,))
                    result = cursor.fetchone()
                    tag_id = result[0] if result else None
                    cursor.execute(
                        """INSERT IGNORE INTO Quote_Tag (quote_id, tag_id) VALUES (%s, %s)""",
                        (quote_id, tag_id),
                    )
        db.commit()

    def get_author_id(self, cursor, name):
        cursor.execute("""SELECT author_id FROM Author WHERE name = (%s)""", (name,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]

    def get_quote(self,cursor, quote_id):
        cursor.execute("""SELECT content FROM Quote WHERE quote_id = (%s)""", (quote_id,))
        return cursor.fetchone()

    def get_quotes_by_author(self, cursor, author_name):
        cursor.execute(
            """SELECT content FROM Quote WHERE author_id = (SELECT author_id FROM Author WHERE name = (%s) )""",
            (author_name,),
        )
        return cursor.fetchall()

    def get_quotes_by_tag(self, cursor, tag):
        cursor.execute(
            """SELECT content FROM Quote WHERE quote_id IN (SELECT quote_id From Quote_Tag WHERE tag_id IN (SELECT tag_id FROM Tag WHERE content = (%s)))""",
            (tag,),
        )
        return cursor.fetchall()

    def get_quotes_by_search_text(self, cursor, search_text):
        cursor.execute(
            """SELECT content FROM Quote WHERE content LIKE (%s)""",
            ("%" + search_text.lower() + "%",),
        )
        return cursor.fetchall()
