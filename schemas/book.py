from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from enum import Enum
from pydantic_mongo import ObjectIdField

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

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BookStatus] = None
    year: Optional[int] = None

class BookResponse(BookBase):
    id: ObjectIdField = Field(alias="_id")
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class PaginatedBooksResponse(BaseModel):
    items: List[BookResponse]
    total: int