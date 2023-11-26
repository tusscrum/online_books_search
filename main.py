# create a database to monogoDB

from fastapi import FastAPI, Depends, Body
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params, paginate
from starlette import status

from control import get_book_info, search_books
from dbs import users_collection, add_or_update_users_books, add_user, \
    fetch_all_books, add_books, fetch_one_user, fetch_one_book, fetch_all_users_books, fetch_one_user_by_id, \
    fetch_one_user_books, update_users_books
from models import Books, UserBooks, UserRegister, UserLogin, CreateBooks

# disable_installed_extensions_check()

app = FastAPI(
    title="Bookstore",
    description="Bookstore API",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redocs",
    openapi_url="/api/openapi.json",

)


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
    books_list = await fetch_all_books()
    return paginate(books_list, parqms)


#

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
        _ = await fetch_one_book(book['isbn'])
        if _:
            books_list.remove(book)
    # remove the duplicate books in list
    books_list = list({v['isbn']: v for v in books_list}.values())

    if await add_books(books_list):
        return paginate(books_list, parqms)
    else:
        return {"message": "Add books failed"}, status.HTTP_404_NOT_FOUND


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
    user_books_list = await fetch_all_users_books(userid)
    return paginate(user_books_list, parqms)


# @app.get('/api/user/books/',
#          response_model=Page[UserBooks],
#          response_model_exclude_unset=True,
#          response_model_exclude_defaults=True,
#          status_code=status.HTTP_200_OK,
#          response_description='Get user\'s books list'
#          )
# async def get_user_books_list(parqms: Params = Depends()):
#     """
#     Get user's books list
#     :return: Page [UserBooks]
#     """
#     user_books_list = await users_books_collection.find().to_list(100)
#     return paginate(user_books_list, parqms)


@app.post('/api/user/{userid}/books',

          response_description='Add book to user\'s books list and some comments'

          )
async def add_book_to_user_books_list(userid: str, user_books: CreateBooks = Body(...)):
    """
    Add book to user's books list
    :return: UserBooks
    """
    # if no user, return 404
    user = await fetch_one_user_by_id(userid)
    if not user:
        return {"message": "User not found"}, status.HTTP_404_NOT_FOUND
    else:

        users_books = jsonable_encoder(user_books)
        user_books = await add_or_update_users_books(users_books)
        return {"message": "Add book to user's books list success", 'user_books': user_books}


@app.put('/api/user/{id}/books/',

         status_code=status.HTTP_201_CREATED,
         response_description='Update book to user\'s books list and some comments'
         )
async def update_book_to_user_books_list(id: str, user_books: CreateBooks = Body(...)):
    """
    Update book to user's books list
    :return: UserBooks
    """
    # if no user, return 404

    book = fetch_one_user_books(id)
    if not book:
        return {"message": "book not found"}, status.HTTP_404_NOT_FOUND
    else:

        user_books = jsonable_encoder(user_books)
        user_books = await update_users_books(id, user_books)
        return {"message": "Update book to user's books list success", 'user_books': user_books}


@app.post('/api/login',
          status_code=status.HTTP_200_OK,
          response_description='Login',
          )
async def login(user: UserLogin = Body(...)):
    """
    Login
    :return: User
    """
    # if no user, return 404

    finded_user = await fetch_one_user(user.username) or await fetch_one_user(user.email)
    if finded_user is None:
        return {"message": "User not found"}, status.HTTP_404_NOT_FOUND

    if finded_user.get('password') == user.password:
        # set session
        return {"message": "Login success", 'user': finded_user}
    else:
        return {"message": "Login failed"}  # , status.HTTP_404_NOT_FOUND


@app.post('/api/register',

          response_description='Register',

          )
async def register(user: UserRegister = Body(...)):
    """
    Register
    :return: User
    """
    # if no user, return 404
    exit_user = await fetch_one_user(user.username) or await fetch_one_user(user.email)
    if exit_user:
        return {"message": "User already exists"}, status.HTTP_404_NOT_FOUND
    else:
        user = jsonable_encoder(user)
        user = await add_user(user)
        return {"message": "Register success", 'user': user}, status.HTTP_201_CREATED


@app.get('/api/user_list',
         response_model=Page[UserRegister],
         )
async def get_user_list(parqms: Params = Depends()):
    """
    Get user list
    :return: Page [User]
    """
    users_list = await users_collection.find().to_list(100)

    return paginate(users_list, parqms)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
