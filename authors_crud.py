from fastapi import FastAPI, APIRouter, Request, status, Body
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from dotenv import dotenv_values
from typing import List
from endpoints.author import router as author_router
from models import Author
from pymongo import MongoClient

app = FastAPI()
config = dotenv_values(".env")
app.include_router()

router = APIRouter()

app.include_router(author_router, tags=["authors"], prefix="/author")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"] + "test"]


@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
    app.database.drop_collection("books")


def test_create_author():
    with TestClient(app) as client:
        response = client.post(
            "/author", json={"name": "Miguel de Cervantes"})
        assert response.status_code == 201

        body = response.json()
        assert body.get("name") == "Miguel de Cervantes"
        assert "_id" in body

def test_create_book_missing_author():
    with TestClient(app) as client:
        response = client.post(
            "/author", json={"author": "Miguel de Cervantes"})
        assert response.status_code == 422


def test_get_author():
    with TestClient(app) as client:
        new_author = client.post(
            "/author", json={"name": "Miguel de Cervantes"}).json()

        get_author_response = client.get("/author" + new_author.get("_id"))
        assert get_author_response.status_code == 200
        assert get_author_response.json() == new_author
