MONGO_HOST = 'localhost'
MONGO_PORT = 27017

MONGO_DBNAME = 'KnockerDB'

DOMAIN = {
    'Jobs': {
        'allow_unknown': True,
        'schema': {
            'title': {'type': 'string'},
            'url': {'type': 'string'},
            'experience': {'type': 'integer'},
            'location': {'type': 'string'},
            'keywords': {'type': 'list'},
            'crawl_id': {'type': 'integer'}
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
    }
}
