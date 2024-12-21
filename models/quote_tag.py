import sqlalchemy as sa
from models.base import Base

class QuoteTag(Base):
    __tablename__ = "quote_tag"
    quote_tag_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    quote_id = sa.Column(sa.Integer, sa.ForeignKey('quote.quote_id', ondelete='CASCADE'), nullable=False)
    tag_id = sa.Column(sa.Integer, sa.ForeignKey('tag.tag_id', ondelete='CASCADE'), nullable=False)
