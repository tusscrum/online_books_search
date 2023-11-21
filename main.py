import os
from typing import List

# create a database to monogoDB
import motor.motor_asyncio
from fastapi import FastAPI
from starlette import status

try:
    from conf import MONGODB_URL
except:
    pass
from control import get_book_info, search_books
from models import Books, User

app = FastAPI(
    title="Bookstore",
    description="Bookstore API",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redocs",

)
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URL') or MONGODB_URL, tls=True,
                                                tlsAllowInvalidCertificates=True)

db = client['college']
books_collection = db.get_collection("books")


# init mongodb


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/api/books_list',
         response_model=List[Books],
         response_model_exclude_unset=True,
         response_model_exclude_defaults=True,
         status_code=status.HTTP_200_OK,
         response_description='Get books list'
         )
async def get_books_list():
    """
    Get books list
    :return: list[Books]
    """
    books_list = await books_collection.find().to_list(100)
    return books_list


@app.post('/api/login',
          status_code=status.HTTP_200_OK,
          response_description='Login',
          )
async def login(user: User):
    """
    Login
    :return: User
    """
    user = await User.objects.get(username=user.username)
    if user.password == user.password:
        # set session
        return {"message": "Login success", 'user': user}
    else:
        return {"message": "Login failed"}


@app.post('/api/register',
          status_code=status.HTTP_201_CREATED,
          response_description='Register',
          )
async def register(user: User):
    """
    Register
    :return: user
    """
    user = await User.objects.get(username=user.username)
    if user:
        return {"message": "User already exists"}, status.HTTP_400_BAD_REQUEST
    else:
        await user.save()
        return {"message": "Register success", 'user': user}, status.HTTP_201_CREATED


@app.get('/api/search',
         response_model=List[Books],
         response_model_exclude_unset=True,
         response_model_exclude_defaults=True,
         status_code=status.HTTP_200_OK,
         response_description='Search books'
         )
async def api_search_books(query: str):
    """
    Search books
    :return: list[Books]
    """
    books_list = await search_books(query)
    # remove the duplicate books in monogoDB
    for book in books_list:
        if await books_collection.find_one({"isbn": book.get('isbn')}) is not None:
            books_list.remove(book)
    await books_collection.insert_many(books_list)
    return books_list


@app.get('/api/books/{isbn}',
         response_model=Books,
         response_model_exclude_unset=True,
         response_model_exclude_defaults=True,
         status_code=status.HTTP_200_OK,
         response_description='Get book by isbn'
         )
async def get_book_by_isbn(isbn: str) -> dict:
    """
    Get book by isbn
    :return: Books
    """
    book = await get_book_info(isbn)
    return book
