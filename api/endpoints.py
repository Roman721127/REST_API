from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from schemas.book import BookCreate, BookResponse
from repository import book_repo
from database import get_db

router = APIRouter()

@router.get("/books", response_model=List[BookResponse])
async def get_books(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db)):
    return await book_repo.get_all_books(db, limit, offset)

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    book = await book_repo.get_book_by_id(db, book_id)
    if not book: raise HTTPException(404)
    return book

@router.post("/books", response_model=BookResponse, status_code=201)
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await book_repo.add_book(db, book.model_dump())

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    await book_repo.delete_book(db, book_id)