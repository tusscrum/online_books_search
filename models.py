"""
@author:liazylee
@license: Apache Licence
@time: 12/11/2023 15:09
@contact: li233111@gmail.com
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from typing import (Optional, Annotated, Any)

from pydantic import (BaseModel, BeforeValidator, Field, EmailStr)

PyObjectId = Annotated[str, BeforeValidator(str)]


class Books(BaseModel):
    """
    BooksModel
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    isbn: str = Field(...)
    title: str = Field(...)
    author: str = Field(...)
    year: str = Field(...)
    image: str = Field(...)
    description: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "isbn": "9781593275846",
                "title": "Eloquent JavaScript, Second Edition",
                "author": "Marijn Haverbeke",
                "year": 2014,
                "image": "https://images-na.ssl-images-amazon.com/images/I/51u8ZRDCVoL._SX377_BO1,"
                         "204,203,200_.jpg",
                "description": "JavaScript lies at the heart of almost every modern web "
                               "application, from social apps "
                               "to the newest browser-based games. Though simple for "
                               "beginners to pick up and play with,"
                               " JavaScript is a flexible, complex language that "
                               "you can use to build full-scale "
                               "applications."
            }
        }

    class Settings:
        name = "books"


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Student created successfully",
                "data": "new_student",
            }
        }


class User(BaseModel):
    """
    User
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(...)
    email: str = EmailStr()
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "liazylee",
                "email": "liazylee@email.com",
                "password": "123456"
            }
        }

    class Settings:
        name = "users"


class UserRegister(BaseModel):
    username: str = Field(...)
    email: str = EmailStr()
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "liazylee",
                "email": "liazylee@gmail.com",
                "password": "123456"
            }
        }


class UserLogin(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "liazylee",
                "password": "123456"
            }
        }


# class BooksCollecion(BaseModel):
#     """
#     BooksCollecion
#     """
#     books: list[Books] = Field(...)
#
#     model_config = {
#         "allow_population_by_field_name": True,
#         "schema_extra": {
#             "example": {
#                 "books": [
#                     {
#                         "isbn": "9781593275846",
#                         "title": "Eloquent JavaScript, Second Edition",
#                         "author": "Marijn Haverbeke",
#                         "year": 2014,
#                         "image": "https://images-na.ssl-images-amazon.com/images/I/51u8ZRDCVoL._SX377_"
#                                  "BO1,204,203,200_.jpg",
#                         "description": "JavaScript lies at the heart of almost every modern "
#                                        "web application, from social apps to the newest browser-based "
#                                        "games. Though simple for beginners to pick up and play with, "
#                                        "JavaScript is a flexible, complex language that you can use to build "
#                                        "full-scale "
#                                        "applications."
#                     },
#                     {
#                         "isbn": "9781449331818",
#                         "title": "Learning JavaScript Design Patterns",
#                         "author": "Addy Osmani",
#                         "year": 2012,
#                         "image": "https://images-na.ssl-images-amazon.com/images/I/51T%2BWt430fL."
#                                  "_SX379_BO1,204,203,200_.jpg",
#                         "description": "With Learning JavaScript Design Patterns,"
#                                        " you’ll learn how to write beautiful, structured, "
#                                        "and maintainable JavaScript by applying classical and"
#                                        " modern design patterns to the language. If you want"
#                                        " to keep your code efficient, more manageable, "
#                                        "and up-to-date with the latest best practices,"
#                                        " this book is for you."
#                     },
#                     {
#                         "isbn": "9781449365035",
#                         "title": "Speaking JavaScript",
#                         "author": "Axel Rauschmayer",
#                         "year": 2014,
#                         "image": "https://images-na.ssl-images-amazon.com/images/"
#                                  "I/51cUVaBWZzL._SX376_BO1,204,203,200_.jpg",
#                         "description": "Like it or not, JavaScript is everywhere "
#                                        "these days—from browser to server to"
#                                        " mobile—and now you, too, need to learn "
#                                        "the language or dive deeper than you have. "
#                                        "This concise book guides you into and through"
#                                        " JavaScript, written by a veteran programmer "
#                                        "who once found himself in the same position."
#                     },
#                     {
#                         "isbn": "978149195029"}
#                 ]
#             }
#         }
#     }


class UserBooks(BaseModel):
    """
    UserBooks
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str = Field(...)
    isbn: str = Field(...)
    title: str = Field(...)
    auothor: str = Field(...)
    year: str = Field(...)
    image: str = Field(...)
    description: str = Field(...)
    status: str = Field(default='reading', choices=['reading', 'read', 'want to read'])
    comment: str = Field(default='')
    rating: int = Field(default=0, gt=0, lt=6)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "user_id": "123456",
                "isbn": "9781593275846",
                "title": "Eloquent JavaScript, Second Edition",
                "author": "Marijn Haverbeke",
                "year": 2014,
                "image": "https://images-na.ssl-images-amazon.com/images/I/51u8ZRDCVoL._SX377_BO1,"
                         "204,203,200_.jpg",
                "description": "JavaScript lies at the heart of almost every modern web "
                               "application, from social apps "
                               "to the newest browser-based games. Though simple for "
                               "beginners to pick up and play with,"
                               " JavaScript is a flexible, complex language that "
                               "you can use to build full-scale "
                               "applications.",
                "status": "reading",
                "comment": "good book",
                "rating": 5
            }
        }
    }


class UpdateUserBooks(BaseModel):
    """
    UpdateUserBooks
    """
    status: str = Field(default='reading', choices=['reading', 'read', 'want to read'])
    comment: str = Field(default='')
    rating: int = Field(default=0, gt=0, lt=6)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "status": "reading",
                "comment": "good book",
                "rating": 5
            }
        }
    }
