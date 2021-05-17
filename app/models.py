import os

import pymongo
from bson import ObjectId
from passlib.hash import pbkdf2_sha256 as sha256


class Mongo:
    """Establishes a connection to the MongoDB instance."""
    def __init__(self, database):
        """
        Establishes a connection to MongoDB.

        :param str database: the name of the collection to connect to.
        """
        mode = os.environ.get("MODE")
        # set mode="dev" for local development, mode="prod" for deployment.
        # connect to mongodb atlas if deployed.
        if mode == "dev":
            mongo_uri = "mongodb://127.0.0.1:27017/"
        else:
            mongo_uri = "mongodb+srv://{user}:{pswd}@cluster0.vte2d.mongodb.net/?retryWrites=true&w=majority".format(
                user=os.environ.get("MONGO_USER"),
                pswd=os.environ.get("MONGO_PSWD"))
        self.db = pymongo.MongoClient(mongo_uri)[database]


# extend Mongo class
class Users(Mongo):
    """Contains all the methods dealing with user management."""
    def __init__(self):
        """Connects to a database, creates one if it does not exist."""
        super(Users, self).__init__("USERS")
        self.db = self.db["ALL_USERS"]

    @staticmethod
    def generate_hash(password):
        """
        Generates a password hash.
        
        :param password: The password to be hashed.
        :type password: str
        :return: hashed_password: The hashed password.
        :rtype: str
        """
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        """
        Verifies the hash generated in generate_hash().

        :param password: The non hashed password to verify.
        :type password: str
        :param hashed_password: The stored password hash.
        :type hashed_password: str
        :return: true/false
        :rtype: boolean
        """
        return sha256.verify(password, hashed_password)

    def save(self, user_details):
        """
        Inserts a single document to the database.

        :param user_details: The JSON sent from api/views.py/AddNewPost()
        :type user_details: str
        """
        self.db.insert_one(user_details)

    def get_user_by_username(self, username):
        """
        Retrieves a single document that matches the given parameter.

        :param username: The Profile to retrieve.
        :type username: str
        :return: user: A MongoDb cursor to the document.
        :rtype: cursor
        """
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

    def get_all_posts(self, limit, last_id=None):
        if last_id is None:
            posts = self.db.find().limit(int(limit))
        else:
            posts = self.db.find({'_id': {'$gt': ObjectId(last_id)}}).limit(int(limit))

        return posts

    def delete_post(self, post_id):
        post = self.db.find_one({"_id": ObjectId(post_id)})
        self.db.delete_one(post)

    def search_post_body(self, query):
        self.db.create_index([("post_body", "text")])
        posts = self.db.find({"$text": {"$search": query}})

        return posts
