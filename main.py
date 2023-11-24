import os

# create a database to monogoDB
import motor.motor_asyncio
from fastapi import FastAPI, Depends
from fastapi_pagination import Page, Params, paginate
from starlette import status

try:
    from conf import MONGODB_URL
except:
    pass
from control import get_book_info, search_books
from models import Books, User, UserBooks

app = FastAPI(
    title="Bookstore",
    description="Bookstore API",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redocs",
    openapi_url="/api/openapi.json",

)
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URL') or MONGODB_URL, tls=True,
                                                tlsAllowInvalidCertificates=True)

db = client['college']
books_collection = db.get_collection("books")


# init mongodb



@app.get('/api/books_list',
         response_model=Page[Books],
         response_model_exclude_unset=True,
         response_model_exclude_defaults=True,
         status_code=status.HTTP_200_OK,
         response_description='Get books list'
         )
async def get_books_list(parqms: Params = Depends()):
    """
    Get books list
    :return: Page [Books]
    """
    books_list = await books_collection.find().to_list(100)
    return paginate(books_list, parqms)


@app.post('/api/login',
          status_code=status.HTTP_200_OK,
          response_description='Login',
          )
async def login(user: User):
    """
    Login
    :return: User
    """
    # if no user, return 404
    user = await User.objects.find_one(username=user.username) or User.objects.find_one(email=user.email) or None
    if not user:
        return {"message": "User not found"}, status.HTTP_404_NOT_FOUND
    if user.password == user.password:
        # set session
        return {"message": "Login success", 'user': user}
    else:
        return {"message": "Login failed"}  # , status.HTTP_404_NOT_FOUND


@app.post('/api/register',
          status_code=status.HTTP_201_CREATED,
          response_description='Register',
          )
async def register(user: User):
    """
    Register
    :return: user
    """
    # if no user, return 404
    user = await User.objects.find_one(username=user.username) or User.objects.find_one(email=user.email) or None
    if user:
        return {"message": "User already exists"}, status.HTTP_404_NOT_FOUND
    else:
        user = await User.objects.create(username=user.username, password=user.password, email=user.email)
        return {"message": "Register success", 'user': user}


@app.get('/api/search',
         response_model=Page[Books],
         response_model_exclude_unset=True,
         response_model_exclude_defaults=True,
         status_code=status.HTTP_200_OK,
         response_description='Search books',

         )
async def api_search_books(query: str, parqms: Params = Depends()):
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
    return paginate(books_list, parqms)


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


# get user's books list
@app.get('/api/user/{userid}/books',
         response_model=Page[UserBooks],
         response_model_exclude_unset=True,
         response_model_exclude_defaults=True,
         status_code=status.HTTP_200_OK,
         response_description='Get user\'s books list'
         )
async def get_user_books_list(userid: str, parqms: Params = Depends()):
    """
    Get user's books list
    :return: Page [UserBooks]
    """
    user_books_list = await UserBooks.objects.find({"userid": userid}).to_list(100)
    return paginate(user_books_list, parqms)


@app.post('/api/user/{userid}/books',
          response_model=UserBooks,
          status_code=status.HTTP_201_CREATED,
          response_description='Add book to user\'s books list and some comments'

          )
async def add_book_to_user_books_list(userid: str, user_books: UserBooks):
    """
    Add book to user's books list
    :return: UserBooks
    """
    # if no user, return 404
    try:
        user = await User.objects.find_one(id=userid)
    except:
        user = None
    if not user:
        return {"message": "User not found"}, status.HTTP_404_NOT_FOUND
    else:
        user_books = await UserBooks.objects.create(userid=userid, isbn=user_books.isbn, comments=user_books.comments,
                                                    rating=user_books.rating, status=user_books.status)
        return {"message": "Add book to user's books list success", 'user_books': user_books}


@app.put('/api/user/{userid}/books/{isbn}',
         response_model=UserBooks,
         status_code=status.HTTP_201_CREATED,
         response_description='Update book to user\'s books list and some comments'
         )
async def update_book_to_user_books_list(userid: str, isbn: str, user_books: UserBooks):
    """
    Update book to user's books list
    :return: UserBooks
    """
    # if no user, return 404
    try:
        user = await User.objects.find_one(id=userid)
    except:
        user = None
    if not user:
        return {"message": "User not found"}, status.HTTP_404_NOT_FOUND
    try:
        book = await books_collection.find_one({"isbn": isbn})
    except:
        book = None
    if not book:
        return {"message": "Book not found"}, status.HTTP_404_NOT_FOUND
    else:
        user_books = await UserBooks.objects.update_one(userid=userid, isbn=isbn, comments=user_books.comments,
                                                        rating=user_books.rating, status=user_books.status)
        return {"message": "Update book to user's books list success", 'user_books': user_books}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
