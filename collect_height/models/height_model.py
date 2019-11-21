from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Height(Base):
    __tablename__ = 'heights'
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True)
    height = Column(Integer)


