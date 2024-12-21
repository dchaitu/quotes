import json
import sqlite3
import os

from constants.constants import get_file_path
from interactors.storage_interface.sqlite_storage_interface import SqliteStorageInterface


class SqliteStorageImplementation(SqliteStorageInterface):

    def create_author_table(self, cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Author
            (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL , 
            born text NOT NULL , 
            reference text UNIQUE NOT NULL
            )"""
        )


    def create_quote_table(self, cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Quote 
            (
            quote_id INTEGER PRIMARY KEY,
            content text,
            author_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES Author(id)

            )"""
        )

    def create_tag_table(self, cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Tag 
            (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content text NOT NULL UNIQUE
            )"""
        )

    def create_quote_tag_table(self, cursor):
        cursor.execute(
        """CREATE TABLE IF NOT EXISTS Quote_Tag 
        (
        tag_id INTEGER ,
        quote_id INTEGER,
        PRIMARY KEY (tag_id, tag_id),
        FOREIGN KEY(tag_id) REFERENCES Tag(tag_id)
        FOREIGN KEY(quote_id) REFERENCES Quote(quote_id)

        )"""
    )


    def insert_authors(self, cursor):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            for author in json_data["authors"]:
                cursor.execute('''INSERT OR IGNORE INTO Author (name, born, reference) VALUES (?, ?, ?)''',
                               (author['name'], author['born'], author['reference']))



    def insert_quotes(self, cursor):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            for quote in json_data["quotes"]:
                author_id = self.get_author_id(cursor, quote['author'])
                cursor.execute('''INSERT OR IGNORE INTO Quote (quote_id, content, author_id) VALUES (?, ?, ?)''',
                               (quote['id'], quote['quote'], author_id))

    def insert_tags(self, cursor):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            for quote in json_data["quotes"]:
                tags = quote['tags']
                for tag in tags:
                    try:
                        cursor.execute('''INSERT OR IGNORE INTO Tag (content) VALUES (?)''', (tag,))
                    except sqlite3.IntegrityError:
                        print(f'{tag} skipped already present')


    def insert_quote_tag(self, cursor):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            for quote in json_data["quotes"]:
                quote_id = quote['id']
                tags = quote['tags']
                for tag in tags:
                    cursor.execute('''SELECT * FROM Tag WHERE content = ?''', (tag,))
                    tag_details = cursor.fetchone()
                    tag_id = tag_details[0] if tag_details != None else None
                    cursor.execute(
                        '''INSERT OR IGNORE INTO Quote_Tag (quote_id, tag_id) VALUES (?, ?)''',
                        (quote_id, tag_id)
                    )

    def get_author_id(self, cursor, name):
        cursor.execute('''SELECT author_id FROM Author WHERE name = (?)''', (name,))
        return cursor.fetchone()[0]

    def get_quote(self, cursor, quote_id):
        cursor.execute('''SELECT content FROM Quote WHERE quote_id = (?)''', (quote_id,))
        return cursor.fetchone()[0]

    def get_quotes_by_author(self, cursor, author_name):
        cursor.execute(
            '''SELECT content FROM Quote WHERE author_id = (SELECT author_id FROM Author WHERE name = (?) )''',
            (author_name,))
        return cursor.fetchall()

    def get_quotes_by_tag(self, cursor, tag):
        cursor.execute(
            '''SELECT content FROM Quote WHERE quote_id IN (SELECT quote_id From Quote_Tag WHERE tag_id IN (SELECT tag_id FROM Tag WHERE content = (?)))''',
            (tag,))
        return cursor.fetchall()

    def get_quotes_by_search_text(self, cursor, search_text):
        cursor.execute('''SELECT content FROM Quote WHERE content LIKE (?)''', ('%' + search_text.lower() + '%',))
        return cursor.fetchall()

