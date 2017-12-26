# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
import datetime
from config import SELECT_BODY, DEVICE, USER_TABLE_NAME, USER_TABLE_FIELD
from pymongo import MongoClient
import os
import redis


class EsToMongodb:
    def __init__(self):
        self.es = Elasticsearch([{"host": os.getenv("ES_HOST", "10.10.1.58"),
                                  "port": int(os.getenv("ES_PORT", "9204"))}])
        self.db = self.get_db()
        self.redis = self.get_redis()
        self.user_field = dict()

    @staticmethod
    def get_db():
        client = MongoClient(os.getenv("DB_HOST", "10.10.1.58"),
                             int(os.getenv("DB_PORT", "27016")))
        db = client.test_database
        return db

    @staticmethod
    def get_redis():
        pool = redis.ConnectionPool(host='redis', port=6379,
                                    decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        return r

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
        result = self.db[USER_TABLE_NAME].insert_one(self.user_field)
        return result

    def get_next_sequence(self, document_name, field_name):

        ret = self.db[document_name].find_and_modify({},
                                                     {'$inc': {field_name: 1}},
                                                     upsert=True, new=True)
        print(ret)
        return ret[field_name]

    def write_data(self, search_user_data):
        for (update_time, platform_type,
             create_time, device_id,
             user_id) in self.build_user_data(search_user_data):

            # save data to redis
            self.redis.set(user_id, create_time)
            # print(self.redis.get(user_id))

            data = self.db[USER_TABLE_NAME].find_one({USER_TABLE_FIELD[1]: int(user_id)})
            if data:
                continue

            self.build_data(platform_type, create_time, device_id, user_id)

            self.write_mongo()
        else:

            update_time = search_user_data['hits']['hits'][-1]['_source']['@timestamp']
            return update_time

    def build_data(self, platform_type, create_time_str, device_id, user_id):

        create_time = (datetime.datetime.strptime(create_time_str,
                                                  "%Y-%m-%d %H:%M:%S")
                       - datetime.timedelta(hours=8))

        sima_id = self.get_next_sequence(document_name='autoid',
                                         field_name=USER_TABLE_FIELD[2])
        self.user_field[USER_TABLE_FIELD[0]] = device_id
        self.user_field[USER_TABLE_FIELD[1]] = int(user_id)
        self.user_field[USER_TABLE_FIELD[2]] = sima_id

        self.user_field[USER_TABLE_FIELD[3]] = create_time
        self.user_field[USER_TABLE_FIELD[4]] = create_time
        self.user_field[USER_TABLE_FIELD[5]] = DEVICE[platform_type]
        self.user_field[USER_TABLE_FIELD[6]] = sima_id

    def redis_update(self):
        for user_id in iter(self.db[USER_TABLE_NAME].distinct(USER_TABLE_FIELD[1])):
            end_time_str = self.redis.get(user_id)
            if end_time_str:
                end_time = (datetime.datetime.strptime(end_time_str,
                                                       '%Y-%m-%d %H:%M:%S') -
                            datetime.timedelta(hours=8))
                self.db[USER_TABLE_NAME].update_one(
                    {USER_TABLE_FIELD[1]: user_id},
                    {'$set': {USER_TABLE_FIELD[4]: end_time}})

    def deal_data(self, yest_stamp, now_stamp):
        while 1:
            user_data = info.get_user_data(yest_stamp, now_stamp)
            # loop write data.
            if user_data['hits']['hits']:
                search_update_time = info.write_data(user_data)

                time_array = (datetime.datetime.strptime(search_update_time,
                                                         "%Y-%m-%dT%H:%M:%S.%fZ")
                              + datetime.timedelta(hours=8))
                yest_stamp = int(time_array.timestamp() * 1000)
            else:
                # redis update data.
                self.redis_update()
                break

if __name__ == "__main__":

    info = EsToMongodb()
    now_time_stamp, yest_time_stamp = info.get_time()

    info.deal_data(yest_time_stamp, now_time_stamp)




