import pymongo, os
from passlib.hash import pbkdf2_sha256 as sha256

class Mongo:
    def __init__(self, database='app'):
        mongo_uri = 'mongodb+srv://{user}:{pswd}@cluster0.vte2d.mongodb.net/?retryWrites=true&w=majority'.format(
            user = os.environ.get('MONGO_USER'),
            pswd = os.environ.get('MONGO_PSWD')
        )
        self.db = pymongo.MongoClient(mongo_uri)[database]

class Users(Mongo):
    def __init__(self):
        super(Users, self).__init__('USERS')
        self.db = self.db['ALL_USERS']

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    def verify_hash(self, password, hashed_password):
        return sha256.verify(password, hashed_password)

    def save(self, user_details):
        self.db.insert_one(user_details)

    def get_user_by_username(self, username):
        user = self.db.find_one(
            {'username': username}
        )
        return user

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
