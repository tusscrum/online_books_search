# create a database to monogoDB

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body
from fastapi_pagination import Page, Params, paginate
from starlette import status

from dbs import books_collection, users_collection, add_user

# disable_installed_extensions_check()

try:
    from conf import MONGODB_URL
except:
    pass
from control import get_book_info, search_books, helper_user
from models import Books, UserRegister, UserLogin

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
    books_list = await books_collection.find().sort('_id', -1).to_list(100)
    return paginate(books_list, parqms)


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

    finded_user = await users_collection.find_one({"username": user.username}) or users_collection.find_one(
        {"email": user.email}) or None
    if not finded_user:
        return {"message": "User not found"}, status.HTTP_404_NOT_FOUND

    if finded_user.get('password') == user.password:

        # set session
        finded_user = helper_user(finded_user)
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
    exit_user = await users_collection.find_one({"username": user.username}) or \
                await users_collection.find_one({"email": user.email}) or None
    if exit_user:
        return {"message": "User already exists"}, status.HTTP_404_NOT_FOUND
    else:
        user = jsonable_encoder(user)
        user = await add_user(user)
        return {"message": "Register success", 'user': user}, status.HTTP_201_CREATED


@app.get('/api/user_list', )
async def get_user_list(parqms: Params = Depends()):
    """
    Get user list
    :return: Page [User]
    """
    users_list = await users_collection.find({}).to_list(100)
    return paginate(users_list, parqms)


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
        _ = books_collection.find_one({"isbn": book.get('isbn')})
        if _:
            books_list.remove(book)
    # remove the duplicate books in list
    books_list = list({v['isbn']: v for v in books_list}.values())

    books_collection.insert_many(books_list)
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
# @app.get('/api/user/{userid}/books',
#          response_model=Page[UserBooks],
#          response_model_exclude_unset=True,
#          response_model_exclude_defaults=True,
#          status_code=status.HTTP_200_OK,
#          response_description='Get user\'s books list'
#          )
# async def get_user_books_list(userid: str, parqms: Params = Depends()):
#     """
#     Get user's books list
#     :return: Page [UserBooks]
#     """
#     user_books_list = await users_books_collection.find({"userid": userid}).to_list(100)
#     return paginate(user_books_list, parqms)


# @app.post('/api/user/{userid}/books',
#           response_model=UserBooks,
#           status_code=status.HTTP_201_CREATED,
#           response_description='Add book to user\'s books list and some comments'
#
#           )
# async def add_book_to_user_books_list(userid: str, user_books: UserBooks = Body(...)):
#     """
#     Add book to user's books list
#     :return: UserBooks
#     """
#     # if no user, return 404
#     _ = users_collection.find_one({"_id": userid})
#     if not _:
#         return {"message": "User not found"}, status.HTTP_404_NOT_FOUND
#     else:
#         users_books = jsonable_encoder(user_books)
#         user_books = add_or_update_users_books(users_books)
#         return {"message": "Add book to user's books list success", 'user_books': user_books}


# @app.put('/api/user/{id}/books/',
#          response_model=UpdateUserBooks,
#          status_code=status.HTTP_201_CREATED,
#          response_description='Update book to user\'s books list and some comments'
#          )
# async def update_book_to_user_books_list(id: str, user_books: UserBooks = Body(...)):
#     """
#     Update book to user's books list
#     :return: UserBooks
#     """
#     # if no user, return 404
#
#     _ = users_books_collection.find_one({"_id": id})
#     if not _:
#         return {"message": "book not found"}, status.HTTP_404_NOT_FOUND
#     else:
#         user_books = jsonable_encoder(user_books)
#         user_books = add_or_update_users_books(user_books)
#         return {"message": "Update book to user's books list success", 'user_books': user_books}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
