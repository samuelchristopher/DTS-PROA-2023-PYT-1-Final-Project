from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str
    year: int = Field(..., gt=0)
    author: str = Field(..., min_length=1)
    publisher: str = Field(..., min_length=1)
