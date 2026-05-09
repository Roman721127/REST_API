from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from models.book import BookORM
from uuid import UUID

async def get_all_books(db: AsyncSession, limit: int, offset: int):
    result = await db.execute(select(BookORM).limit(limit).offset(offset))
    return result.scalars().all()

async def get_book_by_id(db: AsyncSession, book_id: UUID):
    result = await db.execute(select(BookORM).filter(BookORM.id == book_id))
    return result.scalar_one_or_none()

async def add_book(db: AsyncSession, book_data: dict):
    book = BookORM(**book_data)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

async def delete_book(db: AsyncSession, book_id: UUID):
    await db.execute(delete(BookORM).where(BookORM.id == book_id))
    await db.commit()