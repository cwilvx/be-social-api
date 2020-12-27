import pymongo
import app

class Mongo:
    def __int__(self, database='be-social'):
        mongo_uri = app.config_options['MONGO_URI']
        self.mongo = pymongo.MongoClient(mongo_uri)[database]

class Posts(Mongo):
    def __init__(self):
        super(Posts, self).__init__('be-social')
        self.db = self.mongo['posts']

    def save(self, post_details):
        self.db.insert_one(post_details)
