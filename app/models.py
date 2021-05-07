import os

import pymongo
from bson import ObjectId
from passlib.hash import pbkdf2_sha256 as sha256


class Mongo:
    def __init__(self, database="app"):
        mode = os.environ.get("MODE")
        if mode == "dev":
            mongo_uri = "mongodb://127.0.0.1:27017/"
        else:
            mongo_uri = "mongodb+srv://{user}:{pswd}@cluster0.vte2d.mongodb.net/?retryWrites=true&w=majority".format(
                user=os.environ.get("MONGO_USER"),
                pswd=os.environ.get("MONGO_PSWD"))
        self.db = pymongo.MongoClient(mongo_uri)[database]


class Users(Mongo):
    def __init__(self):
        super(Users, self).__init__("USERS")
        self.db = self.db["ALL_USERS"]

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        return sha256.verify(password, hashed_password)

    def save(self, user_details):
        self.db.insert_one(user_details)

    def get_user_by_username(self, username):
        user = self.db.find_one({"username": username})
        return user


class Posts(Mongo):
    def __init__(self):
        """Initialize this class."""
        super(Posts, self).__init__("ALL_POSTS")
        self.db = self.db["POSTS"]

    def insert_post(self, post_details):
        """Insert a single post to the collection."""
        self.db.insert_one(post_details)

    def get_post_by_id(self, post_id):
        post = self.db.find_one({"_id": ObjectId(post_id)})

        return post

    def get_all_posts(self, limix=None, last_id=None):
        if last_id is None:
            posts = self.db.find().limit(limix)
        else:
            posts = self.db.find({'_id': {'$gt': ObjectId(last_id)}}).limit(limix)

        return posts

    def delete_post(self, post_id):
        post = self.db.find_one({"_id": ObjectId(post_id)})
        self.db.delete_one(post)

    def search_post_body(self, query):
        self.db.create_index([("post_body", "text")])
        posts = self.db.find({"$text": {"$search": query}})

        return posts
