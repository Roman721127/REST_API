from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
import jwt

from database import get_db
from schemas.book import BookCreate, BookUpdate, BookResponse, PaginatedBooksResponse
from schemas.user import UserCreate, Token, RefreshTokenReq
from repository import book_repo
from services.auth import (
    get_password_hash, verify_password, create_access_token, 
    create_refresh_token, get_current_user, SECRET_KEY, ALGORITHM
)

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    await db.users.insert_one({"username": user.username, "password": hashed_password})
    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorDatabase = Depends(get_db)):
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {
        "access_token": create_access_token({"sub": user["username"]}),
        "refresh_token": create_refresh_token({"sub": user["username"]}),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh(req: RefreshTokenReq):
    try:
        payload = jwt.decode(req.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
    return {
        "access_token": create_access_token({"sub": username}),
        "refresh_token": create_refresh_token({"sub": username}),
        "token_type": "bearer"
    }


@router.post("/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: AsyncIOMotorDatabase = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await book_repo.create_book(db, book)

@router.get("/books", response_model=PaginatedBooksResponse)
async def get_books(
    limit: int = Query(10, ge=1), 
    offset: int = Query(0, ge=0), 
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    books = await book_repo.get_all_books(db, limit, offset)
    total = await db.books.count_documents({})
    return {"items": books, "total": total}

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user: str = Depends(get_current_user)):
    book = await book_repo.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: str, book: BookUpdate, db: AsyncIOMotorDatabase = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated_book = await book_repo.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user: str = Depends(get_current_user)):
    deleted = await book_repo.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None