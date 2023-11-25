# """
# @author:liazylee
# @license: Apache Licence
# @time: 12/11/2023 19:19
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
#
# from fastapi.testclient import TestClient
#
# from main import app
#
# client = TestClient(app)
#
#
# def test_search_books():
#     response = client.get("/api/search?query=python")
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#     print(response.json())
