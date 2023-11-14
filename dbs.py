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
# import os
#
# # create a database to monogoDB
# import motor.motor_asyncio
#
# from conf import MONGODB_URL
#
#
# class DataBase:
#
#     def __init__(self):
#         self.uri = os.environ.get('MONGODB_URL') or MONGODB_URL
#         self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri, tls=True, tlsAllowInvalidCertificates=True)
#
#         self.db = self.client.college
#         self.books_collection = self.db.get_collection("books")
#
#     def new_book(self, book_data: dict) -> dict:
#         """
#         Create a new book
#         :param book_data: dict
#         :return: dict
#         """
#         return self.books_collection.insert_one(book_data)
#
#     def get_book(self, isbn: int) -> dict:
#         """
#         Get a book by isbn
#         :param isbn: int
#         :return: dict
#         """
#         return self.books_collection.find_one({"isbn": isbn})
#
#     def get_books(self) -> list[dict]:
#         """
#         Get all books
#         :return: list
#         """
#         books = self.books_collection.find()
#         return books
#
#     def insert_many(self, data: list[dict]) -> list[dict]:
#         """
#         Insert many data
#         :param data: list
#         :return: list
#         """
#         return self.books_collection.insert_many(data)
#
#
# mongodb = DataBase()
