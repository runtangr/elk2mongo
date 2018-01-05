
from datetime import datetime

from mongoengine import *

from .auto_id import AutoId

from pj.sync.core.init_database import r_user
from pj.sync.config import USER_TABLE_FIELD


class BUser48971(Document):

    device_id = IntField()
    user_id = IntField()
    sima_id = IntField()
    first_visit_time = DateTimeField()
    last_visit_time = DateTimeField()
    platform = IntField()
    update_time = DateTimeField(default=datetime.utcnow())

    meta = {
        "collection": "b_user_48971",
        'indexes': ['user_id']
    }

    @classmethod
    def add(cls, user_field):
        item = cls.get(user_field[USER_TABLE_FIELD[1]])
        if not item:
            # update sima id
            # sima_obj = AutoId.get()
            sima_obj = AutoId.add()

            user_field[USER_TABLE_FIELD[2]] = sima_obj.sima_id
            item = cls(**user_field)
            item.save()
        return item

    @classmethod
    def get(cls, user_id):
        rs = r_user.get(user_id)
        if rs:
            return cls.from_json(rs)
        try:
            item = cls.objects(user_id=user_id).first()
        except DoesNotExist:
            pass
        else:
            if item:
                r_user.set(user_id, item.to_json())
                return item

    @classmethod
    def set_endtime_redis(cls, user_field):
        item = cls(**user_field)
        r_user.set(user_field[USER_TABLE_FIELD[1]], item.to_json())

    @classmethod
    def update_endtime(cls, user_id, end_time):
        item = cls.objects(user_id=user_id).first()
        item[USER_TABLE_FIELD[4]] = end_time
        # update redis. redis data need equal mongodb
        r_user.set(user_id, item.to_json())

        item.save()


