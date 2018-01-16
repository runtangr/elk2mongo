# -*- coding:utf-8 -*-

import datetime
from .config import SELECT_SESSION_BODY, CSV_FIELD, DEVICE, CSV_DIR, CSV_FILE_NAME
import os
import json
from .core.init_database import es
import time
from .utils import get_yest_str
import csv


class EsToCSV:
    def __init__(self):
        self.es = es
        self.csv_field = dict()
        self.csv_file_path = os.path.join(CSV_DIR, CSV_FILE_NAME.format(get_yest_str()))
        self.init_csv_file()

    def init_csv_file(self):
        if os.path.exists(CSV_DIR) is False:
            os.mkdir(CSV_DIR)
        with open(self.csv_file_path, 'a') as csv_file:

            writer = csv.DictWriter(csv_file, list(CSV_FIELD))

            field_dict = {key: key for key in CSV_FIELD}
            writer.writerow(field_dict)

    @staticmethod
    def get_time():
        today = datetime.date.today()
        yes_day = datetime.date.today() - datetime.timedelta(days=1)
        now_stamp = int(time.mktime(today.timetuple()) * 1000)
        yest_stamp = int(time.mktime(yes_day.timetuple()) * 1000)
        return now_stamp, yest_stamp

    def get_session_data(self, yest_stamp, now_stamp):
        SELECT_SESSION_BODY["post_filter"]["range"]["@timestamp"]["gt"] = yest_stamp
        SELECT_SESSION_BODY["post_filter"]["range"]["@timestamp"]["lte"] = now_stamp
        datas = self.es.search(body=SELECT_SESSION_BODY)

        # print(datas)
        return datas

    def parse_session_data(self, datas):
        for hits in datas:
            if 'data' not in hits['_source']['myroot']:
                continue
            for data in hits['_source']['myroot']['data']:
                if '_功能编码' in data['pr'] and '$cuid' in data['pr']:
                    self.csv_field[CSV_FIELD[0]] = int(data['pr']['$cuid'])
                    self.csv_field[CSV_FIELD[1]] = hits['_source']['myroot']['ut']
                    self.csv_field[CSV_FIELD[2]] = data['pr']['$eid']
                    if 'ip' in hits['_source']['myroot']:
                        self.csv_field[CSV_FIELD[3]] = hits['_source']['myroot']['ip']
                    else:
                        self.csv_field[CSV_FIELD[3]] = '0.0.0.0'
                    self.csv_field[CSV_FIELD[4]] = DEVICE[hits['_source']['myroot']['pl']]
                    self.csv_field[CSV_FIELD[5]] = int(data['pr']['_功能编码'])

                    yield self.csv_field

    def write_session_data(self):
        with open(self.csv_file_path, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, list(CSV_FIELD))
            writer.writerow(self.csv_field)

    def deal_data(self, yest_stamp, now_stamp):
        while 1:
            session_datas = self.get_session_data(yest_stamp, now_stamp)
            # loop write data.
            if session_datas['hits']['hits']:
                for _ in self.parse_session_data(session_datas['hits']['hits']):
                    self.write_session_data()

                time_array = (datetime.datetime.strptime(
                    session_datas['hits']['hits'][-1]['_source']['@timestamp'],
                    "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8))
                yest_stamp = int(time_array.timestamp() * 1000)
            else:
                break


if __name__ == "__main__":

    session_obj = EsToCSV()
    now_time_stamp, yest_time_stamp = session_obj.get_time()
    session_obj.deal_data(yest_time_stamp, now_time_stamp)
