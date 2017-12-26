import unittest
from sync.sync_mongo import EsToMongodb


class SyncMongo(unittest.TestCase):

    def test_get_next_sequence(self):
        es_mongo = EsToMongodb()
        es_mongo.get_next_sequence(document_name='autoid',
                                   field_name='simaid')
