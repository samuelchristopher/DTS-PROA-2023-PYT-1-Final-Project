from pydantic import BaseModel


class Book(BaseModel):
    title: str
    year: int
    author: str
    publisher: str
