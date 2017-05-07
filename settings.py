MONGO_HOST = 'localhost'
MONGO_PORT = 27017

MONGO_DBNAME = 'KnockerDB'

XML = False
CACHE_CONTROL='no-cache'
IF_MATCH = False
X_DOMAINS = '*'
X_HEADERS = ['Content-Type']

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
        'resource_methods': ['GET', 'POST', 'DELETE'],
        'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
        'schema': {
            'uid': {'type': 'string'},
            'job': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'Jobs',
                    'field': '_id',
                    'embeddable': True
                }
            }
        }
    }
}
