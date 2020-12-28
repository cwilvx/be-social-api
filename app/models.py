import pymongo
from bson.json_util import dumps, loads

mongo_uri = None

def configure_stuff(app):
    global mongo_uri
    mongo_uri = app.config['MONGO_URI']

class Mongo:
    def __init__(self, database='be-social'):
        self.db = pymongo.MongoClient(mongo_uri)[database]

class Posts(Mongo):
    def __init__(self):
        super(Posts, self).__init__('be-social')
        self.db = self.db['posts']

    def save(self, post_details):
        self.db.insert_one(post_details)

    def get_post_by_body(self, post_body):
        post = self.db.find_one(
            {'post_body': post_body}
        )
        return post
    def get_all_posts(self):
        posts_cursor = self.db.find()
        posts_list = list(posts_cursor)
        posts_json = dumps(posts_list)
        return posts_json
