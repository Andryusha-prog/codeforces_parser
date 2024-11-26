from sqlalchemy import Column, Integer, VARCHAR, String, TEXT
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class ProblemsTable(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True, index=True)
    contestId = Column(Integer)
    index = Column(VARCHAR)
    name = Column(String)
    rating = Column(Integer)
    tags = Column(TEXT)

class StatisticsTable(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True, index=True)
    contestId = Column(Integer)
    index = Column(VARCHAR)
    solvedCount = Column(Integer)