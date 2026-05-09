from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.book import BookORM
from schemas.book import BookCreate
from typing import Optional
from uuid import UUID

async def get_all_books(db: AsyncSession, limit: int, cursor: Optional[UUID] = None):
    stmt = select(BookORM).order_by(BookORM.id).limit(limit)
    if cursor:
        stmt = stmt.where(BookORM.id > cursor)
    
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_book(db: AsyncSession, book: BookCreate):
    new_book = BookORM(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book