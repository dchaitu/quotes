import json


from constants.constants import get_file_path
from interactors.storage_interface.storage_interface import SqlAlchemyStorageInterface
from models.author import Author
from models.quote import Quote
from models.quote_tag import QuoteTag
from models.tag import Tag



class  SqlAlchemyStorageImplementation(SqlAlchemyStorageInterface):
    def insert_authors(self, session):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            existing_authors = {author.name for author in session.query(Author).all()}
            author_objs = []
            seen_authors = set()
            for author in json_data["authors"]:
                if author["name"] not in existing_authors and author["name"] not in seen_authors:
                    author_objs.append(Author(name=author["name"], born=author["born"], reference=author["reference"]))
                    seen_authors.add(author["name"])

        if author_objs:
            session.bulk_save_objects(author_objs)
            session.commit()

    def insert_quotes(self, session):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            existing_quotes = {quote.content for quote in session.query(Quote).all()}
            author_map = {author.name: author.author_id for author in session.query(Author).all()}

            quotes = []
            seen_quotes = set()
            for quote in json_data["quotes"]:
                print(quote)
                if quote["quote"] not in existing_quotes and quote["quote"] not in seen_quotes:
                    author_id = author_map.get(quote['author'])
                    if author_id:  # Only add if author exists
                        quotes.append(
                            Quote(
                                content=quote["quote"],
                                author_id=author_id
                            )
                        )
            if quotes:
                session.bulk_save_objects(quotes)
                session.commit()

    def insert_tags(self, session):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            for quote in json_data["quotes"]:
                tags = quote["tags"]
                for tag in tags:
                    if not session.query(Quote).filter_by(content=tag).first():
                        query = Tag(content=tag)
                        session.add(query)
                session.commit()

    def insert_quote_tag(self, session):
        file_path = get_file_path()
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            for quote in json_data["quotes"]:
                quote_id = quote["id"]
                tags = quote["tags"]
                for tag in tags:
                    query = session.query(Tag).filter_by(content=tag).first()
                    if query:
                        result = session.query(Tag).filter_by(content=query.content).first()
                        tag_id = result.tag_id if result else None
                        print(f"tag_id: {tag_id}")
                        query = QuoteTag(tag_id=tag_id, quote_id=quote_id)
                        session.add(query)
                session.commit()

    def get_author_id(self, session, author_name):
        author = session.query(Author).filter_by(name=author_name).first()
        return author.author_id


    def get_quote(self, session, quote_id):
        query = session.query(Quote).filter_by(quote_id=quote_id).first()
        result = query.content
        return result

    def get_quotes_by_author(self, session, author_name):
        query = session.query(Quote.content).join(Author).filter(Author.name == author_name).all()

        quote_list = [result[0] for result in query]
        return quote_list

    def get_quotes_by_tag(self, session, tag):
        query = (session.query(Quote.content).join(QuoteTag, Quote.quote_id == QuoteTag.quote_id)\
                   .join(Tag,QuoteTag.tag_id == Tag.tag_id).filter(
            Tag.content == tag).all())
        quote_list = [result[0] for result in query]

        return quote_list


    def get_quotes_by_search_text(self, session, search_text):
        query = session.query(Quote.content).filter(Quote.content.like(f'%{search_text}%'))
        quote_list = [result[0] for result in query]
        return quote_list





