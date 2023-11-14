"""
@author:liazylee
@license: Apache Licence
@time: 13/11/2023 20:51
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
from pymongo import MongoClient

from conf import MONGODB_URL

client = MongoClient(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)
db = client['test']  # database name
collection = db['books']


def test_mongodb():
    post = {'_id': 0, 'name': 'Jeff', 'score': 9}
    collection.insert_one(post)
    collection.find_one({'name': 'Jeff'})
    one = collection.find_one({'name': 'Jeff'})
    collection.update_one({'name': 'Jeff'}, {'$set': {'score': 10}})
    collection.delete_one({'name': 'Jeff'})
