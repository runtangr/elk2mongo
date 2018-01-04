import redis
from mongoengine import connect
from elasticsearch import Elasticsearch

# init mongodb, redis, elasticsearch
connect(host='mongodb', db='test_database')

ES = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

pool_user = redis.ConnectionPool(host='redis', port=6379, db=0)
r_user = redis.StrictRedis(connection_pool=pool_user)

pool_sima = redis.ConnectionPool(host='redis', port=6379, db=1)
r_sima = redis.StrictRedis(connection_pool=pool_sima)