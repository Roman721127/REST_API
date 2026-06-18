from fastapi import APIRouter, Depends, Query, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_db
from schemas.book import BookCreate, BookUpdate, BookResponse, PaginatedBooksResponse
from repository import book_repo

router = APIRouter()

@router.post("/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await book_repo.create_book(db, book)

@router.get("/books", response_model=PaginatedBooksResponse)
async def get_books(
    limit: int = Query(10, ge=1), 
    offset: int = Query(0, ge=0), 
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    books = await book_repo.get_all_books(db, limit, offset)
    total = await db.books.count_documents({})
    return {"items": books, "total": total}

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    book = await book_repo.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: str, book: BookUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    updated_book = await book_repo.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    deleted = await book_repo.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None