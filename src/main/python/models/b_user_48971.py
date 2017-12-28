
from datetime import datetime

from mongoengine import *
from config import USER_TABLE_FIELD
from models.auto_id import AutoId
from core.core import r


class BUser48971(Document):

    device_id = IntField()
    user_id = IntField()
    sima_id = IntField()
    begin_date = DateTimeField()
    end_date = DateTimeField()
    platform = IntField()
    update_time = DateTimeField(default=datetime.now)

    meta = {
        "collection": "b_user_48971",
        'indexes': ['user_id']
    }

    @classmethod
    def add(cls, user_field):
        item = cls.get(user_field[USER_TABLE_FIELD[1]])
        if not item:
            # update sima id
            sima_obj = AutoId.get()
            sima_obj.sima_id += 1
            sima_obj.save()

            item = cls(**user_field)
            item.save()
        return item

    @classmethod
    def get(cls, user_id):
        rs = r.get(user_id)
        if rs:
            return cls.from_json(rs)
        try:
            item = cls.objects(user_id=user_id).first()
        except DoesNotExist:
            pass
        else:
            if item:

                r.set(user_id, item.to_json())
                return item

    @classmethod
    def set_endtime_redis(cls, user_field):
        item = cls(**user_field)
        r.set(user_field[USER_TABLE_FIELD[1]], item.to_json())

    @classmethod
    def update_endtime(cls, user_id, end_time):
        item = cls.objects(user_id=user_id).first()
        item.end_date = end_time
        item.save()


