import pymongo

mongo_uri = None

def configure_stuff(app):
    global mongo_uri
    mongo_uri = app.config['MONGO_URI']

class Mongo:
    def __init__(self, database='be-social'):
        self.mongo = pymongo.MongoClient(mongo_uri)[database]

class Posts(Mongo):
    def __init__(self):
        super(Posts, self).__init__('be-social')
        self.db = self.mongo['posts']

    def save(self, post_details):
        self.db.insert_one(post_details)
