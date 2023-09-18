import uuid
from typing import Optional
from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    title: str
    page_number: str

class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    page_number: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "page_number": 200,
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    page_number: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "page_number": 200,
            }
        }


class Author(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f7e",
                "name": "Miguel de Cervantes",
            }
        }
