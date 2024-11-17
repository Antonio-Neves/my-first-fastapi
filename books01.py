from fastapi import Body, FastAPI

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

app = FastAPI()


@app.get('/books')
async def read_all_books():
    return BOOKS


# @app.get('/books/{first_book}')
# async def read_first_book():
#     return {'first_book': BOOKS[0]}


# @app.get('/books/{book_choice}')
# async def read_book_choice(book_choice):
#     return {'book_choice': book_choice}


# @app.get('/books/{first_book}')
# async def read_first_book():
#     return {'first_book': BOOKS[0]}


@app.get('/books/categories')
def list_categories():
    result = set()

    for book in BOOKS:
        result.add(book['category'])

    return result


@app.get('/books/')
def book_category(category_choice: str):
    list_books = []

    for book in BOOKS:
        if book.get('category').casefold() == category_choice.casefold():
            list_books.append(book)

    return list_books


@app.get('/books/{book_author_category}')
def book_author_category_by_query(book_author: str, category: str):
    list_books = []

    for book in BOOKS:

        if book['author'].casefold() == book_author and \
                book['category'].casefold() == category.casefold():

            list_books.append(book)

    return list_books


# @app.get('/books/{chose_title}')
# def book_title(title: str):
#
#     for book in BOOKS:
#         if book.get('title').casefold() == title.casefold():
#             return book


@app.post('/books/create_new_book')
def create_new_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put('/books/update_book_category')
def update_book_category(book_to_update=Body()):

    for book in range(len(BOOKS)):
        if book_to_update.get('title').casefold() == BOOKS[book].get('title').casefold():
            BOOKS[book] = book_to_update




