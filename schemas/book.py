from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

class BookBase(BaseModel):
    title: str = Field(..., description="Назва книги")
    author: str
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID
    class Config:
        from_attributes = True