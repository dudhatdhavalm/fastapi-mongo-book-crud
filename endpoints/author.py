from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Author

router = APIRouter()

@router.post("", response_description="Create a new author", status_code=status.HTTP_201_CREATED, response_model=Author)
def create_author(request: Request, author: Author = Body(...)):
    author = jsonable_encoder(author)
    new_author = request.app.database["author"].insert_one(author)
    created_author = request.app.database["author"].find_one(
        {"_id": new_author.inserted_id}
    )

    return created_author


@router.get("", response_description="List all author", response_model=List[Author])
def list_author(request: Request):
    author = list(request.app.database["author"].find(limit=100))
    return author