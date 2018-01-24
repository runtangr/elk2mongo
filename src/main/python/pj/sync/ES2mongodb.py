# -*- coding:utf-8 -*-

import datetime

from .config import SELECT_USER_BODY, DEVICE, USER_TABLE_FIELD
from .core.init_database import r_user, es
import json
import time

from .models.b_user_48971 import BUser48971


class EsToMongodb:
    def __init__(self):

        self.es = es
        # elasticsearch
        self.user_field = dict()

    @staticmethod
    def get_time():
        today = datetime.date.today()
        yes_day = datetime.date.today() - datetime.timedelta(days=1)
        now_stamp = int(time.mktime(today.timetuple()) * 1000)
        yest_stamp = int(time.mktime(yes_day.timetuple()) * 1000)
        return now_stamp, yest_stamp

    def get_user_data(self, yest_stamp, now_stamp):

        SELECT_USER_BODY["post_filter"]["range"]["@timestamp"]["gt"] = yest_stamp
        SELECT_USER_BODY["post_filter"]["range"]["@timestamp"]["lte"] = now_stamp
        datas = self.es.search(body=SELECT_USER_BODY)

        # print(datas)
        return datas

    @staticmethod
    def build_user_data(datas):
        for hits in datas['hits']['hits']:
            if 'data' not in hits['_source']['myroot']:
                continue
            for data in hits['_source']['myroot']['data']:
                if '$cr' in data['pr'] and '$cuid' in data['pr']:

                    try:
                        uid = int(data['pr']['$cuid'])
                        device_id = int(data['pr']['$cr'])
                    except ValueError:
                        continue

                    yield (hits['_source']['@timestamp'],
                           hits['_source']['myroot']['pl'],
                           hits['_source']['myroot']['ut'],
                           data['pr']['$cr'], data['pr']['$cuid'])

    def write_data(self, search_user_data):
        for (update_time, platform_type,
             create_time, device_id,
             user_id) in self.build_user_data(search_user_data):

            self.build_data(platform_type, create_time, device_id, user_id)

            BUser48971.add(self.user_field)
            # update redis user endtime
            BUser48971.set_endtime_redis(self.user_field)

        else:

            update_time = search_user_data['hits']['hits'][-1]['_source']['@timestamp']
            return update_time

    def build_data(self, platform_type, create_time_str, device_id, user_id):

        create_time = (datetime.datetime.strptime(create_time_str,
                                                  "%Y-%m-%d %H:%M:%S")
                       - datetime.timedelta(hours=8))

        # sima_id = self.get_next_sequence(document_name='autoid',
        #                                  field_name=USER_TABLE_FIELD[2])
        self.user_field[USER_TABLE_FIELD[0]] = int(device_id)
        self.user_field[USER_TABLE_FIELD[1]] = int(user_id)

        self.user_field[USER_TABLE_FIELD[3]] = create_time
        self.user_field[USER_TABLE_FIELD[4]] = create_time
        self.user_field[USER_TABLE_FIELD[5]] = DEVICE[platform_type]

    def endtime_update(self):
        for user_id in iter(BUser48971.objects.distinct('user_id')):
            user_obj = r_user.get(user_id)
            user_dict = json.loads(user_obj)

            end_time = (datetime.datetime.utcfromtimestamp(
                user_dict[USER_TABLE_FIELD[4]]['$date']/1000))

            BUser48971.update_endtime(user_id, end_time)

    def deal_data(self, yest_stamp, now_stamp):
        while 1:
            user_data = self.get_user_data(yest_stamp, now_stamp)
            # loop write data.
            if user_data['hits']['hits']:
                search_update_time = self.write_data(user_data)

                time_array = (datetime.datetime.strptime(search_update_time,
                                                         "%Y-%m-%dT%H:%M:%S.%fZ")
                              + datetime.timedelta(hours=8))
                yest_stamp = int(time_array.timestamp() * 1000)
            else:
                # redis update data.
                self.endtime_update()
                break

if __name__ == "__main__":

    info = EsToMongodb()
    now_time_stamp, yest_time_stamp = info.get_time()

    info.deal_data(yest_time_stamp, now_time_stamp)




