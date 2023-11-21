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
import os

from pymongo import MongoClient

try:
    from conf import MONGODB_URL
except:
    pass

client = MongoClient(MONGODB_URL or os.environ.get('MONGODB_URL'), tls=True, tlsAllowInvalidCertificates=True)
db = client['test']  # database name
collection = db['books']


def test_mongodb():
    post = {'_id': 0, 'name': 'Jeff', 'score': 9}
    collection.insert_one(post)
    collection.find_one({'name': 'Jeff'})
    _ = collection.find_one({'name': 'Jeff'})
    collection.update_one({'name': 'Jeff'}, {'$set': {'score': 10}})
    collection.delete_one({'name': 'Jeff'})
