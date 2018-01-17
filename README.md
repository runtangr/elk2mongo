
# 主要需求
      从elk获取数据，过滤需求数据存储mongodb

# 主要实现目标
      1.获取elasticsearch指定时间段数据，如一天 循环增量获取
      2.解析数据，组合数据
      3.redis缓存数据
      4.存储数据到mongodb(ORM)

# 主要技术
      elasticsearch(通过docker-compose配置连接外部elk网络)
      mongodb(orm)
      redis(缓存)
      celery

# 生产环境使用
      sh start.sh

# 测试环境使用
      安装虚拟环境 virtualenv
      python 版本 3.+
      安装需求包 requirements.txt
      配置数据库:
         修改 ./src/main/python/sync/core/init_database.py
         初始化 mongodb, redis, elasticsearch
      celery运行方式:
         cd ./src/main/python/
         celery -A pj worker -B -Q es_mongodb,mongodb_json -l info
      一般运行方式:
         cd ./src/main/python/
         python pj/sync/ES2mongodb.py && python pj/sync/mongodb2json.py

# 各主要文件作用
      src/main/python/sync/config.py
         配置elasticsearch、 mongodb、 csv相关信息

      src/main/python/sync/core
         初始化数据库配置

      src/main/python/sync/models
         mongodb ORM表结构定义，和对应表操作定义

      src/main/python/sync/ES2mongodb.py
         从elasticsearch 获取和过滤数据到mongodb

      src/main/python/sync/mongodb2json.py
         从mongodb 获取数据到json文件

      src/main/python/sync/ES2csv.py
         从elasticsearch 获取和过滤数据,存储本地csv文件

      src/main/python/sync/csv2ftp.py
         本地csv文件上传到ftp服务器