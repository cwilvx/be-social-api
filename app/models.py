import pymongo, os

class Mongo:
    def __init__(self, database='app'):
        mongo_uri = 'mongodb+srv://{user}:{pswd}@cluster0.vte2d.mongodb.net/?retryWrites=true&w=majority'.format(
            user = os.environ.get('MONGO_USER'),
            pswd = os.environ.get('MONGO_PSWD')
        )
        self.db = pymongo.MongoClient(mongo_uri)[database]

class Posts(Mongo):
    def __init__(self):
        super(Posts, self).__init__('ALL_POSTS')
        self.db = self.db['POSTS']

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
