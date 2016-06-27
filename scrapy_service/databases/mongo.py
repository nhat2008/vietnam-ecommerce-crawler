__author__ = 'nhat'

from pymongo import MongoClient
from scrapy.conf import settings

class Mongodb():
    client = None
    rel_coll = None

    def __init__(self, host='localhost', port=27017, db=None, col=None):
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        self._client = MongoClient(host, port)
        self._db = self._client[db]
        self.name_col = col
        self.rel_coll = self._db[col]

    def refresh_collection(self):
        self.rel_coll.drop()
        self.rel_coll = self._db[self.name_col]

    def save(self, data_dict):
        self.rel_coll.update_one({'name': data_dict['name']}, {'$set': data_dict}, upsert=True)

    def check_and_save_link(self, link_name):
        if self.rel_coll.find_one({"link": link_name}):
            return False
        self.rel_coll.insert({'link': link_name})
        return True

    def index(self, field):
        self.rel_coll.create_index(field)
        