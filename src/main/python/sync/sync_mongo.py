# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
import datetime
from config import SELECT_BODY, DEVICE
from pymongo import MongoClient
import os


class EsToMongodb:
    def __init__(self):
        self.es = Elasticsearch([{"host": os.getenv("ES_HOST","10.10.1.58"),
                                  "port": int(os.getenv("ES_PORT","9204"))}])
        self.db = self.get_db()
        self.user_field = dict()

    @staticmethod
    def get_db():
        client = MongoClient(os.getenv("DB_HOST", "10.10.1.58"),
                             int(os.getenv("DB_PORT", "27016")))
        db = client.test_database
        return db

    @staticmethod
    def get_time():
        now_stamp = int(datetime.datetime.now().timestamp() * 1000)
        yest_stamp = int((datetime.datetime.now() -
                          datetime.timedelta(days=1)).timestamp() * 1000)
        return now_stamp, yest_stamp

    def get_user_data(self, yest_stamp, now_stamp):

        SELECT_BODY["post_filter"]["range"]["@timestamp"]["gt"] = yest_stamp
        SELECT_BODY["post_filter"]["range"]["@timestamp"]["lte"] = now_stamp
        datas = self.es.search(body=SELECT_BODY)

        print(datas)
        return datas

    @staticmethod
    def build_user_data(datas):
        for hits in datas['hits']['hits']:

            for data in hits['_source']['myroot']['data']:
                if '$cr' and '$cuid' not in data['pr']:
                    break
                else:
                    yield (hits['_source']['@timestamp'],
                           hits['_source']['myroot']['sdk'],
                           hits['_source']['myroot']['ut'],
                           data['pr']['$cr'], data['pr']['$cuid'])

    def write_mongo(self):
        result = self.db['user'].insert_one(self.user_field)
        return result

    def get_next_sequence(self, document_name, field_name):

        ret = self.db[document_name].find_and_modify({}, {'$inc': {field_name: 1}}, upsert=True, new=True)
        print(ret)
        return ret[field_name]

    def write_data(self, search_user_data):
        for (update_time, device_type,
             create_time, device_id, user_id) in self.build_user_data(search_user_data):

            self.user_field['userId'] = int(user_id)
            data = self.db['user'].find_one({'userId': int(user_id)})
            if data:
                continue

            self.build_data(device_type, create_time, device_id)

            self.write_mongo()
        else:
            return update_time

    def build_data(self, device_type, create_time_str, device_id):

        create_time = datetime.datetime.strptime(create_time_str, "%Y-%m-%d %H:%M:%S")

        sima_id = self.get_next_sequence(document_name='autoid',
                                         field_name='simaid')
        self.user_field['deviceType'] = DEVICE[device_type]
        self.user_field['createTime'] = create_time
        self.user_field['deviceId'] = int(device_id)
        self.user_field['simaId'] = sima_id

    def deal_data(self, yest_stamp, now_stamp):
        while 1:
            user_data = info.get_user_data(yest_stamp, now_stamp)
            if user_data['hits']['hits']:
                search_update_time = info.write_data(user_data)

                time_array = (datetime.datetime.strptime(search_update_time,
                                                         "%Y-%m-%dT%H:%M:%S.%fZ")
                              + datetime.timedelta(hours=8))
                yest_stamp = int(time_array.timestamp() * 1000)
            else:
                break

if __name__ == "__main__":

    info = EsToMongodb()
    now_time_stamp, yest_time_stamp = info.get_time()

    info.deal_data(yest_time_stamp, now_time_stamp)




