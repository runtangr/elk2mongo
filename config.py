DEVICE = {
  "zg_android": 1
}

USER_TABLE_NAME = 'b_user_48971'

USER_TABLE_FIELD = ('device_id', 'user_id',
                    'sima_id', 'begin_date',
                    'end_date', 'platform',
                    '_id')

SELECT_BODY = {
  "query": {
    "term": {
       "message": "zg_android"
    }
  },
  "post_filter": {
    "range": {
      "@timestamp": {
        "gt": 1,
        "lte": 2
      }
    }
  },
  "_source": ["@timestamp", "myroot.data.pr.$cr",
              "myroot.data.pr.$cuid", "myroot.ut", "myroot.sdk"],
  "size": 5,
  "sort": [
    {
      "@timestamp": {
        "order": "asc"
      }
    }
  ]
}

