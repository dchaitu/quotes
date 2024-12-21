import sqlalchemy as sa
from models.base import Base

class Tag(Base):
    __tablename__ = "tag"

    tag_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    content = sa.Column(sa.String(50))