from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

#BOOK OBJECT CREATOR
class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, book_id, title, author, description, rating, published_date):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

#BOOK CREATION VALIDATION
class BookRequest(BaseModel):
    book_id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0,lt=6)
    published_date: int = Field(gt=1999,lt=2031)

    class Config:
        json_schema_extra={
                "example": {
                "title":"Title of the Book",
                "author":"name of the author",
                "description":"description of the book",
                "rating": 5,
                "published_date": 1999
                }
            }

#BOOK LIST
BOOKS = [
    Book(1,"Computer Science Pro","codingwithroby","Avery nice book!",5,2005),
    Book(2,"Be Fast with Fast API","codingwithroby","Avery great book!",5,2007),
    Book(3,"Master Endpoints","codingwithroby","Avery awsome book!",5,2009),
    Book(4,"HP1","Author1","book!",5,2030),
    Book(5,"HP2","Author2","book!",2,2031),
    Book(6,"HP3","Author3","book!",3,2029),
    Book(7,"HP4","Author3","book!",1,2027),
    Book(8,"HP5","Author4","book!",4,2026)
]

#READ ALL BOOKS
@app.get("/books")
async def read_all_books():
    return BOOKS

#SEARCH BOOK WITH BOOK ID
@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

#SEARCH WITH RATINGS/ QUERY VALIDATION
@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

#SEARCH WITH PUBLISHED DATE/ PATH VALIDATION
@app.get("/books/publish/")
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

#NEW BOOK CREATION
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(findbook_id(new_book))

#ID SERIES CREATION
def findbook_id(book: Book):
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
    return book

#UPDATE BASED ON ID
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book.book_id:
            BOOKS[i] = Book(**book.model_dump())
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")

#DELETE BASED ON ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book_id:
            BOOKS.pop(i)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")
