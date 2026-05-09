from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from enum import Enum

class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: BookStatus
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedBooksResponse(BaseModel):
    items: List[BookResponse]
    next_cursor: Optional[UUID] = None