from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Book:

    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):

        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create.', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int  = Field(gt=1500, lt=3000)  # = Field(min_length=4, max_length=4)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "António Calheiros Neves",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2024
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2024),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2000),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2015),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2023),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2023),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2024)
]


@app.get('/books', status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS


@app.get('/books/{book_id}')
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail='Item not found')


@app.get('/books/', status_code=status.HTTP_200_OK)
def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    books_by_rating = []
    for book in BOOKS:
        if book.rating == rating:
            books_by_rating.append(book)

    return books_by_rating


@app.get('/books/published_date/', status_code=status.HTTP_200_OK)
def read_published_date(published_date: int = Query(gt=1500, lt=3000)):
    books_by_published_date = []

    for book in BOOKS:
        if book.published_date == published_date:
            books_by_published_date.append(book)

    return books_by_published_date


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())

    print(type(new_book))
    print(new_book)

    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):

    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')








