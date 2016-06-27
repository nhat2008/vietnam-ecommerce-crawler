__author__ = 'nhat'

from elasticsearch import Elasticsearch
import json
from scrapy.conf import settings

class ES():
    def __init__(self, host='localhost', port=9200, index=None, doc_type=None):
        host = settings['ES_SERVER']
        port = settings['ES_PORT']
        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.index = index
        self.doc_type = doc_type
        self.id = 0

    def save(self, data_dict):
        self.id +=1
        self.es.index(index=self.index, doc_type=self.doc_type, body=data_dict)

    def get_byID(self, data_id):
        res = es.get(index=self.index, doc_type=self.doc_type, id=data_id)
        return res