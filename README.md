
# 主要需求
      从elk获取数据，过滤需求数据存储mongodb

# 主要实现目标
      1.获取elasticsearch指定时间段数据，如一天 循环增量获取
      2.解析数据，组合数据
      3.redis缓存数据
      4.存储数据到mongodb(ORM)

# 主要技术
      elasticsearch(通过docker-compose配置连接外部elk网络)
      mongoengine
      redis