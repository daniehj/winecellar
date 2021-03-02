from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import DateTime
from .database import Base


class Record(Base):
    __tablename__ = 'temperatures'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True,nullable=True)
    date = Column(DateTime,index=True)
    loc = Column(String(255), index=True)
    temperature = Column(Float)
