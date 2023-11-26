# """
# @author:liazylee
# @license: Apache Licence
# @time: 25/11/2023 22:02
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
from fastapi.testclient import TestClient

from main import app


def test_mock_add_books():
    response = TestClient(app).post("/api/user/65627084602dfa97f3e85d95/books", json={
        "user_id": "65627084602dfa97f3e85d95",
        "isbn": "9781593276614",
        "title": "Eloquent JavaScript, Second Edition",
        "author": "Marijn Haverbeke",
        "year": "2014",
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
    })
    print(response.json())
    assert response.status_code == 200
