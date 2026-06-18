from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.book import BookCreate, BookUpdate
from bson import ObjectId

async def get_all_books(db: AsyncIOMotorDatabase, limit: int, offset: int):
    cursor = db.books.find({}).skip(offset).limit(limit)
    return await cursor.to_list(length=limit)

async def get_book_by_id(db: AsyncIOMotorDatabase, book_id: str):
    return await db.books.find_one({"_id": ObjectId(book_id)})

async def create_book(db: AsyncIOMotorDatabase, book: BookCreate):
    book_dict = book.model_dump()
    result = await db.books.insert_one(book_dict)
    book_dict["_id"] = result.inserted_id
    return book_dict

async def update_book(db: AsyncIOMotorDatabase, book_id: str, book: BookUpdate):
    update_data = {k: v for k, v in book.model_dump().items() if v is not None}
    if update_data:
        await db.books.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})
    return await get_book_by_id(db, book_id)

async def delete_book(db: AsyncIOMotorDatabase, book_id: str):
    result = await db.books.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count > 0