MONGO_HOST = 'localhost'
MONGO_PORT = 27017

MONGO_DBNAME = 'KnockerDB'

XML = False

X_DOMAINS = '*'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

DOMAIN = {
    'Jobs': {
        'allow_unknown': True,
        'schema': {
            'title': {'type': 'string'},
            'url': {'type': 'string'},
            'experience': {'type': 'integer'},
            'location': {'type': 'string'},
            'keywords': {'type': 'list'},
            'crawl_id': {'type': 'integer'},
            'categories': {'type': 'integer'},
            'company': {'type': 'string'}
        },
        'mongo_indexes': {
            'text':
                [('location', 'text')]
        }
    },
    'crawl': {
        'schema': {
            'crawl_id': {'type': 'integer'}
        }
    },
    'pinnedJobs': {
        'allow_unknown': True,
        'schema': {
            'uid': {'type': 'string'},
            'jobId': {'type': 'objectid'}
        },
        'datasource': {
            'aggregation': {
                'pipeline': [
                    {'$lookup': {'from': 'Jobs', 'localField': 'jobId', 'foreignField': '_id', 'as': 'job'}},
                    {'$unwind': '$job'}
                ]
            }
        }
    }
}
