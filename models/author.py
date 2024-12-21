from models.base import Base
import sqlalchemy as  sa

class Author(Base):
    __tablename__ = "author"

    author_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    born = sa.Column(sa.String(100))
    reference = sa.Column(sa.String(100), unique=True)