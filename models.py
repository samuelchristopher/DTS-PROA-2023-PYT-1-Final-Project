from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy.sql import func


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))
