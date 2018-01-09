# -*- coding:utf-8 -*-


DEVICE = {
  "and": 1,
  "js": 3
}

USER_TABLE_NAME = 'b_user_48971'

USER_TABLE_FIELD = ('device_id', 'user_id',
                    'sima_id', 'first_visit_time',
                    'last_visit_time', 'platform', 'update_time')

SELECT_USER_BODY = {
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


SELECT_SESSION_BODY = {
                          "query": {
                            "terms": {
                              "myroot.pl": [
                                "js",
                                "and"
                              ]
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
                          "_source": ["myroot.data.pr.$cuid", "myroot.ut",
                                      "myroot.data.pr.$eid", "myroot.sdk",
                                      "myroot.data.pr ._功能编码", "@timestamp"],
                          "size": 5
                        }

