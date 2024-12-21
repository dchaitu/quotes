import sqlalchemy as sa
from models.base import Base

class Quote(Base):
    __tablename__ = "quote"

    quote_id = sa.Column(sa.Integer, primary_key=True,autoincrement=True)
    content = sa.Column(sa.String(200))
    author_id = sa.Column(sa.Integer, sa.ForeignKey('author.author_id', ondelete='CASCADE'), nullable=False)
