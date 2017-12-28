DEVICE = {
  "and": 1,
  "js": 1
}

USER_TABLE_NAME = 'b_user_48971'

USER_TABLE_FIELD = ('device_id', 'user_id',
                    'sima_id', 'begin_date',
                    'end_date', 'platform')

SELECT_BODY = {
                "query": {
                  "terms": {
                     "myroot.pl": ["js", "and"]
                  }
                },
                "post_filter": {
                  "range": {
                    "@timestamp": {
                      "gte": 1,
                      "lte": 2
                    }
                  }
                },
                "sort": [
                  {
                    "@timestamp": {
                      "order": "asc"
                    }
                  }
                ],
                "_source": ["myroot.data.pr.$cuid", "myroot.data.pr.$cr",
                            "@timestamp", "myroot.pl", "myroot.ut"],
                "size": 5
              }

