
from mongoengine import *


class AutoId(Document):

    sima_id = IntField(default=0)

    meta = {
        "collection": "auto_id",
        'indexes': ['sima_id']
    }

    @classmethod
    def add(cls, sima_id):

        item = cls(sima_id=sima_id)
        item.save()
        return item

    @classmethod
    def get(cls):

        item = cls.objects().first()
        return item




