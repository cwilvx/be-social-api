import pymongo, os

mongo_uri = None

def configure_stuff(app):
    global mongo_uri
    mongo_uri = app.config['MONGO_URI']

class Mongo:
    def __init__(self, database='USERS'):
        self.db = pymongo.MongoClient(mongo_uri)[database]

class Posts(Mongo):
    def __init__(self):
        super(Posts, self).__init__('USERS')
        self.db = self.db['ALL_POSTS']

    def save(self, post_details):
        self.db.insert_one(post_details)

    def get_post_by_body(self, post_body):
        post = self.db.find_one(
            {'post_body': post_body}
        )
        return post
    def get_all_posts(self):
        posts = self.db.find()
        return posts
