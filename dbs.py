# """
# @author:liazylee
# @license: Apache Licence
# @time: 12/11/2023 14:54
# @contact: li233111@gmail.com
# # code is far away from bugs with the god animal protecting
#     I love animals. They taste delicious.
#               ┏┓      ┏┓
#             ┏┛┻━━━┛┻┓
#             ┃      ☃      ┃
#             ┃  ┳┛  ┗┳  ┃
#             ┃      ┻      ┃
#             ┗━┓      ┏━┛
#                 ┃      ┗━━━┓
#                 ┃  神兽保佑    ┣┓
#                 ┃　永无BUG！   ┏┛
#                 ┗┓┓┏━┳┓┏┛
#                   ┃┫┫  ┃┫┫
#                   ┗┻┛  ┗┻┛
# """
import os

import motor.motor_asyncio
from bson import ObjectId

from conf import MONGODB_URL
from control import helper_user, helper_user_books, helper_books

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URL') or MONGODB_URL, tls=True,
                                                tlsAllowInvalidCertificates=True)

db = client['college']
books_collection = db.get_collection("books")
users_collection = db.get_collection("users")
users_collection.create_index("email", unique=True)
users_books_collection = db.get_collection("users_books")


async def fetch_one_book(isbn: str) -> dict:
    """
    Fetch one book
    :param isbn: str
    :return: dict
    """
    book = await books_collection.find_one({"isbn": isbn})
    if book:
        return helper_books(book)


async def fetch_all_books():
    """
    Fetch all books
    :return: list
    """
    books = []
    __books = books_collection.find()
    for book in __books:
        books.append(helper_books(book))
    return books


async def add_books(books: list[dict]) -> bool:
    """
    Add book
    :param books: dict
    :return: dict
    """
    _ = await books_collection.insert_many(books)
    if _:
        return True
    else:
        return False


async def add_user(user: dict) -> dict:
    """
    Add user
    :param user: dict
    :return: dict
    """

    result = await users_collection.insert_one(user)

    new_user = await users_collection.find_one({"_id": result.inserted_id})
    return helper_user(new_user)


async def fetch_one_user(username: str) -> dict:
    find_user = await users_collection.find_one({"username": username}) \
                or await users_collection.find_one({"email": username})
    if find_user:
        return helper_user(find_user)


async def fetch_one_user_by_id(user_id: str) -> dict:
    find_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if find_user:
        return helper_user(find_user)


async def add_or_update_users_books(user_books: dict) -> dict:
    """
    Add user's books
    :param user_books: dict
    :return: dict
    """
    exit_user_books = await users_books_collection.find_one({"user_id": user_books['user_id'],
                                                             "isbn": user_books['isbn']})
    if exit_user_books:
        await users_books_collection.update_one({"user_id": user_books['user_id'],
                                                 "isbn": user_books['isbn']},
                                                {"$set": {"status": user_books['status'],
                                                          "rating": user_books['rating'],
                                                          "comment": user_books['comment']}})
        new_user_books = await users_books_collection.find_one({"user_id": user_books['user_id'],
                                                                "isbn": user_books['isbn']})
    else:
        result = await users_books_collection.insert_one(user_books)
        new_user_books = await users_books_collection.find_one({"_id": result.inserted_id})
    print(new_user_books)
    return helper_user_books(new_user_books)


async def update_users_books(id: str, user_books: dict) -> dict:
    exit_user_books = await users_books_collection.find_one({"_id": ObjectId(id)})
    if exit_user_books:
        await users_books_collection.update_one({"_id": ObjectId(id)},
                                                {"$set": {"status": user_books['status'],
                                                          "rating": user_books['rating'],
                                                          "comment": user_books['comment']}})
        new_user_books = await users_books_collection.find_one({"_id": ObjectId(id)})
        return helper_user_books(new_user_books)


async def fetch_one_user_books(id: str) -> dict:
    find_user_books = await users_books_collection.find_one({"_id": ObjectId(id)})
    if find_user_books:
        return helper_user_books(find_user_books)


async def fetch_all_users_books(user_id: str) -> list[dict]:
    """
    Fetch all user's books
    :param user_id: str
    :return: list
    """
    user_books = []
    async for user_book in users_books_collection.find({"user_id": user_id}).sort({"_id": -1}):
        user_books.append(helper_user_books(user_book))
    return user_books
