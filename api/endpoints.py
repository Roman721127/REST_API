from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.book import BookCreate, BookResponse, PaginatedBooksResponse
from repository import book_repo
from typing import Optional
from uuid import UUID

router = APIRouter()

@router.post("/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await book_repo.create_book(db, book)

@router.get("/books", response_model=PaginatedBooksResponse)
async def get_books(
    limit: int = Query(10, ge=1), 
    cursor: Optional[UUID] = None, 
    db: AsyncSession = Depends(get_db)
):
    books = await book_repo.get_all_books(db, limit, cursor)
    
    next_cursor = books[-1].id if len(books) == limit else None
    
    return {"items": books, "next_cursor": next_cursor}