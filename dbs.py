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

from conf import MONGODB_URL
from control import helper_user

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URL') or MONGODB_URL, tls=True,
                                                tlsAllowInvalidCertificates=True)

db = client['college']
books_collection = db.get_collection("books")
books_collection.create_index("isbn", unique=True)
users_collection = db.get_collection("users")
users_collection.create_index("email", unique=True)
users_books_collection = db.get_collection("users_books")
users_books_collection.create_index("user_id", unique=True)
users_books_collection.create_index("book_id", unique=True)


async def add_user(user: dict) -> dict:
    """
    Add user
    :param user: dict
    :return: dict
    """

    result = await users_collection.insert_one(user)

    new_user = await users_collection.find_one({"_id": result.inserted_id})
    return helper_user(new_user)
