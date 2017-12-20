import unittest
from sync import sync_mongo
es_mongo = sync_mongo.EsToMongodb()


class SyncMongo(unittest.TestCase):

    def test_get_next_sequence(self):
        es_mongo.get_next_sequence(document_name='autoid',
                                   field_name='simaid')
