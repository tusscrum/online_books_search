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

import aiohttp

from conf import GOOGLE_BOOKS_API_KEY


# use google books api to get the book information

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
            return response.get('items', [])[0].get('volumeInfo', {})


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
            print(response)
            response = await get_response_to_model(response.get('items', []))

            # save this item into monogoDB
            return response


async def get_response_to_model(response: dict) -> list[dict]:
    """
    Get response to model
    :param json: dict
    :return: dict
    """
    res = []
    for item in response:
        res_dict = {}
        res_dict['isbn'] = item['volumeInfo'].get('industryIdentifiers', [])[0].get('identifier', '')
        res_dict['title'] = item['volumeInfo'].get('title', '')
        res_dict['author'] = ','.join(item['volumeInfo'].get('authors', []))
        res_dict['year'] = item['volumeInfo'].get('publishedDate', '')
        res_dict['image'] = item['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
        res_dict['description'] = item['volumeInfo'].get('description', '')
        res.append(res_dict)
        logging.info(res_dict, 'res_dict')
    return res
