from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import uuid4
import random
import json
import os

app = FastAPI()

BOOKS_DATABASE = []
BOOKS_FILE = "books.json"

if os.path.isfile(BOOKS_FILE):
    with open(BOOKS_FILE, 'r') as f:
        BOOKS_DATABASE = json.load(f)

class Book(BaseModel):
    name: str
    price: float
    book_id: Optional[str]
    genre: Literal["fiction","non-fiction"]

@app.get("/")
async def home():
    return {"message":"Welcome to me FastAPI Bookstore!"}

@app.get("/list-books")
async def list_books():
    return {"books": BOOKS_DATABASE}

@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
    if index < 0 or index >= len(BOOKS_DATABASE):
        raise HTTPException(status_code=404, detail="Error! Book not found")
    return {"book": BOOKS_DATABASE[index]}

@app.get("/get-random-book")
async def get_random_book():
    return {"book": random.choice(BOOKS_DATABASE)}

@app.post("/add-book", response_model=Book)
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOKS_DATABASE.append(json_book)
    with open(BOOKS_FILE, "w") as json_file:
        json.dump(BOOKS_DATABASE, json_file, indent=4)
    return book

@app.get("/get-book/{book_id}")
async def get_book(book_id: str):
    for book in BOOKS_DATABASE:
        if book["book_id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Error! Book not found")
