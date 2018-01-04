
from mongoengine import *
import sys
sys.path.insert(0, '..')
from core.init_database import r_sima


class AutoId(Document):

    sima_id = IntField(default=0)

    meta = {
        "collection": "auto_id",
        'indexes': ['sima_id']
    }

    @classmethod
    def add(cls):
        item = cls.get()
        # update redis and mongodb
        if item:
            item.sima_id += 1
            item.save()
        else:
            # first save and add
            item = cls(sima_id=1)
            item.save()
        return item

    @classmethod
    def get(cls):
        rs = r_sima.get("sima_id")
        if rs:
            return cls.from_json(rs)
        try:
            item = cls.objects().first()
        except DoesNotExist:
            pass
        else:
            if item:
                r_sima.set("sima_id", item.to_json())
                return item





