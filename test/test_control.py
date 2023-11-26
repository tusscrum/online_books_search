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
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


async def test_get_book_info():
    response = await client.get("/api/books/9787115428028/")
    assert response.status_code == 200
    assert response.json() == {
        "isbn": "9787115428028",
        "title": "Python编程快速上手",
        "subtitle": "让繁琐工作自动化",
        "author": "Al Sweigart",
        "published": "2015-12-01",
        "publisher": "人民邮电出版社",
        "pages": 496,
        "description": "《Python编程快速上手 让繁琐工作自动化》是一本面向初学者的Python编程入门书籍。全书共分为15章，内容包括Python基础知识、流程控制、函数、列表、字典、字符串、正则表达式、文件操作、异常处理、调试、Web编程、Excel、PDF和Word文档、电子邮件、GUI编程、数据结构和算法。书中的每一章都包含练习题，读者可以通过练习题来巩固所学知识。本书适合初学者阅读，也适合有一定基础的Python爱好者阅读。",
        "website": "http://www.ituring.com.cn/book/1861",
        "cover": "https://img3.doubanio.com/view/subject/l/public/s28381798.jpg",
        "comments": []
    }


