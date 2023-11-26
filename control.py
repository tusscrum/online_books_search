"""
@author:liazylee
@license: Apache Licence
@time: 12/11/2023 18:46
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
import logging
import os

import aiohttp

try:
    from conf import MONGODB_URL, GOOGLE_BOOKS_API_KEY
except:
    pass

GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY') or GOOGLE_BOOKS_API_KEY


# use Google books api to get the book information
async def get_book_info(isbn: str) -> dict:
    """
    Get book info by isbn
    :param isbn: str
    :return: dict
    """
    # Read API key from env variable

    # Query the api with key and ISBN as parameters
    async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(
                f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={GOOGLE_BOOKS_API_KEY}") as response:
            response = await response.json()
            response = await get_isbn_to_model(response)
            return response


async def search_books(query: str) -> list[dict]:
    """
    Search books
    :param query: str
    :return: dict
    """
    # Read API key from env variable
    async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(
                f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}") as response:
            response = await response.json()
         
            response = await get_response_to_model(response.get('items', []))

            # save this item into monogoDB
            return response


async def get_isbn_to_model(response: dict) -> dict:
    """
    Get response to model
    :param response:
    :return:
    """
    res_dict = {}
    response = response['items'][0].get('volumeInfo', {})
    res_dict['isbn'] = response.get('industryIdentifiers', [])[0].get('identifier', '')
    res_dict['title'] = response.get('title', '')
    res_dict['author'] = ','.join(response.get('authors', []))
    res_dict['year'] = response.get('publishedDate', '')
    res_dict['image'] = response.get('imageLinks', {}).get('thumbnail', '')
    res_dict['description'] = response.get('description', '')
    return res_dict


async def get_response_to_model(response: dict) -> list[dict]:
    """
    Get response to model
    :param json: dict
    :return: dict
    """
    res = []
    for item in response:
        res_dict = {}
        industryIdentifiers = item['volumeInfo'].get('industryIdentifiers', [])
        if len(industryIdentifiers) == 0:
            res_dict['isbn'] = ''
        else:
            res_dict['isbn'] = industryIdentifiers[0].get('identifier', '')
        res_dict['title'] = item['volumeInfo'].get('title', '')
        res_dict['author'] = ','.join(item['volumeInfo'].get('authors', []))
        res_dict['year'] = item['volumeInfo'].get('publishedDate', '')
        res_dict['image'] = item['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
        res_dict['description'] = item['volumeInfo'].get('description', '')
        res.append(res_dict)
        logging.debug(res_dict, 'res_dict')
    return res


def helper_user(user: dict) -> dict:
    """
    Helper user
    :param user: dict
    :return: dict
    """
    return {
        "id": str(user.get('_id')),
        "username": user.get('username'),
        "email": user.get('email'),
        "password": user.get('password')
    }


def helper_user_books(user_books: dict, ) -> dict:
    """
    Helper user's books
    :param user_books: dict
    :return: dict
    """
    return {
        "id": str(user_books.get('_id')),
        "user_id": user_books.get('user_id'),
        'isbn': user_books.get('isbn'),
        'title': user_books.get('title'),
        'author': user_books.get('author'),
        'year': user_books.get('year'),
        'image': user_books.get('image'),
        'description': user_books.get('description'),
        'status': user_books.get('status'),
        'comment': user_books.get('comment'),
        'rating': user_books.get('rating'),
    }


def helper_books(book: dict) -> dict:
    """
    Helper books
    :param book: dict
    :return: dict
    """
    return {
        "id": str(book.get('_id')),
        'isbn': book.get('isbn'),
        'title': book.get('title'),
        'author': book.get('author'),
        'year': book.get('year'),
        'image': book.get('image'),
        'description': book.get('description'),
    }
