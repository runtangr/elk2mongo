import redis
from mongoengine import connect
# init mongodb and redis
connect('test_database')
pool_user = redis.ConnectionPool(host='localhost', port=6379, db=0)
r_user = redis.StrictRedis(connection_pool=pool_user)

pool_sima = redis.ConnectionPool(host='localhost', port=6379, db=1)
r_sima = redis.StrictRedis(connection_pool=pool_sima)