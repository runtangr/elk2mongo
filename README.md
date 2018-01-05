
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

# 生产环境使用
      sh start.sh

# 测试环境使用
      安装虚拟环境 virtualenv
      python 版本 3.+
      安装需求包 requirements.txt
      配置数据库:
         修改 ./src/main/python/sync/core/init_database.py
         初始化 mongodb, redis, elasticsearch
      程序运行:
         cd ./src/main/python/sync/
         python ES2mongo.py

# 各主要文件作用