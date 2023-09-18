from fastapi import APIRouter, Body, Request, Response, HTTPException, status , Depends
from fastapi.encoders import jsonable_encoder
from typing import List, Union, Dict, Any
# from crud.crud_book import book as book_create
from crud.crud_book import CRUDBook

from models import Book, BookUpdate , BookCreate
router = APIRouter()

@router.post("", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
# def create_book(request: Request, book: Book ,book_crud: CRUDBook = Depends()):
    # first
    # book = jsonable_encoder(book)
    # new_book = request.app.database["books"].insert_one(book)
    # created_book = request.app.database["books"].find_one(
    #     {"_id": new_book.inserted_id}
    # )
    # return created_book


#testing chatgpt
def create_book(request: Request, book: BookCreate ,book_crud: CRUDBook = Depends()):
    created_book = book_crud.create(db=request.app.database["books"],obj_in=book)
    if created_book:
        return created_book
    else:
        raise HTTPException(status_code=500, detail="Failed to create book")
     
   
    # db = request.app.database["books"]
    # crud = CRUDBook()
    # create_book = crud.create(db=db,obj_in=book)
    # if create_book:
    #     return create_book
    # raise HTTPException(status_code=500, detail="Book creation failed")


@router.get("", response_description="List all books", response_model=List[Book])
# actual
# def list_books(request: Request):
    # books = list(request.app.database["books"].find(skip=0, limit=100))
    # return books

#testing chatgpt
def list_books(request: Request,book_crud: CRUDBook = Depends()):
    # Call the get_multi method from your MongoDB wrapper
    books = book_crud.get_multi(request=request)
    return books



@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with ID {id} not found")


@router.put("/{id}", response_description="Update a book", response_model=Book)
# def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
#     book = {k: v for k, v in book.dict().items() if v is not None}
#     if len(book) >= 1:
#         update_result = request.app.database["books"].update_one(
#             {"_id": id}, {"$set": book}
#         )
#         if update_result.modified_count == 0:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")
#     if (
#         existing_book := request.app.database["books"].find_one({"_id": id})
#     ) is not None:
#         return existing_book
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

# def update_mongodb_book(request: Request, db_obj: Book, obj_in: Union[Book, Dict[str, Any]]):
#     collection = request.app.database["books"]
#     if isinstance(obj_in, Book):
#         obj_in = obj_in.__dict__
#     collection.update_one({"_id": db_obj["_id"]}, {"$set": obj_in})
#     return db_obj

def update(request: Request, *, db_obj: Book, obj_in: Union[Book, Dict[str, Any]]) -> Book:
    collection_name = "books"
    collection = request.app.database[collection_name]

    if isinstance(obj_in, Book):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)

    update_query = {"$set": update_data}

    collection.update_one({"_id": db_obj.id}, update_query)

    return db_obj

@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    delete_result = request.app.database["books"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with ID {id} not found")
