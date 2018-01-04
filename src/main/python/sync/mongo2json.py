from models.b_user_48971 import BUser48971
from core.init_database import r_user
import json
import datetime
from config import USER_TABLE_FIELD

def build_data(user_str):
    user_dict = json.loads(user_str)
    user_dict['_id'] = user_dict['_id']['$oid']
    user_dict[USER_TABLE_FIELD[3]] = datetime.datetime.fromtimestamp(
        user_dict[USER_TABLE_FIELD[3]]['$date']/1000).strftime('%Y-%m-%d %H:%M:%S')

    user_dict[USER_TABLE_FIELD[4]] = datetime.datetime.fromtimestamp(
        user_dict[USER_TABLE_FIELD[4]]['$date']/1000).strftime('%Y-%m-%d %H:%M:%S')

    user_dict[USER_TABLE_FIELD[6]] = datetime.datetime.fromtimestamp(
        user_dict[USER_TABLE_FIELD[6]]['$date']/1000).strftime('%Y-%m-%d %H:%M:%S')

    user_data = json.dumps(user_dict)

    return user_data


def user2json():
    # get all use_id from redis
    keys = r_user.keys()
    for user_id in keys:
        user_data = BUser48971.get(user_id)
        user_str = user_data.to_json()
        user_build = build_data(user_str)
        with open('./user_json/b_user_48971.json', 'a') as f:
            f.writelines(''.join([user_build, '\n']))


def init_file():
    # create or overlay file
    with open('./user_json/b_user_48971.json', 'w') as f:
        pass

if __name__ == "__main__":
    init_file()
    user2json()
