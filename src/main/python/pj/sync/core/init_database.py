import redis
from mongoengine import connect
from elasticsearch import Elasticsearch

# init mongodb, redis, elasticsearch
connect(host='localhost', db='test_database')

es = Elasticsearch([{'host': '10.3.131.170', 'port': 9204}])

pool_user = redis.ConnectionPool(host='localhost', port=6379, db=0)
r_user = redis.StrictRedis(connection_pool=pool_user)

pool_sima = redis.ConnectionPool(host='localhost', port=6379, db=1)
r_sima = redis.StrictRedis(connection_pool=pool_sima)