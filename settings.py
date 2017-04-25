MONGO_HOST = 'localhost'
MONGO_PORT = 27017

MONGO_DBNAME = 'KnockerDB'

DOMAIN = {
    'Jobs': {
        'schema': {
            'title': {'type': 'string'},
            'url': {'type': 'string'},
            'experience': {'type': 'integer'},
            'location': {'type': 'string'},
            'crawl_id': {'type': 'integer'}
        }
    },
    'crawl': {
        'schema': {
            'crawl_id': {'type': 'integer'}
        }
    }
}
