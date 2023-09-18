from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder
from models import Book , BookCreate
from datetime import date
from fastapi import Request
from typing import List
from pymongo import MongoClient

class CRUDBook:
    # first
    # def create(self, book: Book) -> Book:
    #     book_dict = book.dict()
    #     book_id = self.collection.insert_one(book_dict).inserted_id
    #     return Book(**book_dict, id=str(book_id))

    # def create(self, request: Request, obj_in: Book) -> Book:
    #     book_obj = jsonable_encoder(obj_in)
    #     result = request.app.database["books"].insert_one(book_obj)
    #     if result.inserted_id:
    #         book_obj["_id"] = result.inserted_id
    #         return Book(**book_obj)
    #     return None

    # def create(self, request: Request, obj_in: Book) -> Book:
    #     collection = request.app.database["books"]
    #     book_obj = jsonable_encoder(obj_in)
    #     result = collection.insert_one(book_obj)
    #     book_obj["_id"] = result.inserted_id
    #     return book_obj

    def create(self, db: MongoClient, *, obj_in: BookCreate) -> dict:
        db_obj = {
            "title": obj_in.title,
            "pages": obj_in.page_number,
        }
        db.books.insert_one(db_obj)
        return db_obj

    # def get_multi(self, request: Request, skip: int = 0, limit: int = 100,) -> List[Book]:
    # collection = request.app.database["books"]
    # documents = collection.find(skip=skip, limit=limit)
    # books = list(documents)
    # return books
    def get_multi(self, request: Request) -> List[Book]:
        collection = request.app.database["books"]

        pipeline = [
            {
                "$lookup": {
                    "from": "author",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author",
                }
            },
            {"$unwind": "$author"},
            {
                "$project": {
                    "id": 1,
                    "title": 1,
                    "pages": 1,
                    "author_id": 1,
                    "author_name": "$author.name",
                }
            },
        ]

        # books = [Book(**data) for data in collection.aggregate(pipeline)]
        # books = list(collection.aggregate(pipeline))
        print(Book(**data) for data in collection.aggregate(pipeline))
        print(collection.aggregate(pipeline))
        return []


book = CRUDBook()
