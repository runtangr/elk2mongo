import redis
from mongoengine import connect
# init mongodb and redis
connect('test_database')
pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.StrictRedis(connection_pool=pool)