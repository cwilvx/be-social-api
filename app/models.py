import os

import pymongo
from bson import ObjectId
from passlib.hash import pbkdf2_sha256 as sha256


class Mongo:
    """Establishes a connection to a MongoDB instance."""
    def __init__(self, database):
        """
        Establishes a connection to MongoDB.

        :param database: the name of the collection to connect to.
        :type database: str
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

        :param user_details: The JSON sent from auth/views/UserRegistration()
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
    """Contains all the methods related with posts management."""
    def __init__(self):
        """Connects to a database, creates one if it does not exist."""
        super(Posts, self).__init__("ALL_POSTS")
        self.db = self.db["POSTS"]

    def insert_post(self, post_details):
        """
        Inserts a single document sent from api/views/AddNewPost() in the database.

        :param post_details: JSON sent from the view.
        :type post_details: JSON
        """
        self.db.insert_one(post_details)

    def get_post_by_id(self, post_id):
        """
        Returns a single document matching the passed id.

        :param post_id: The MongoDB _oid of the document to retrieve.
        :type post_id: str
        :return: post: The cursor to the document matching the query.
        :rtype: cursor
        """
        post = self.db.find_one({"_id": ObjectId(post_id)})

        return post

    def get_all_posts(self, limit, last_id=None):
        """
        Returns all the posts in the database, based on the limit and the last_id.

        :param limit: The number of documents to retrieve.
        :type limit: num
        :param last_id: The MongoDB _oid of the last document in the previous page, for paging purposes.
        :type last_id: str
        :return: posts: The MongoDb cursor to the documents.
        :rtype: cursor
        """

        # check whether it's first page
        if last_id is None:
            posts = self.db.find().limit(int(limit))
        else:
            # get all posts greater than the _oid
            posts = self.db.find({'_id': {'$gt': ObjectId(last_id)}}).limit(int(limit))

        return posts

    def delete_post(self, post_id):
        """
        Deletes a single document matching the MongoDb _oid provided.

        :param post_id: The MongoDb _oid sent from the request.
        :type post_id: str
        """
        post = self.db.find_one({"_id": ObjectId(post_id)})
        self.db.delete_one(post)

    def search_post_body(self, query):
        """
        Returns a list of documents matching the search query.

        :param query: The string to search for in the database.
        :type query: str
        :return: posts: A cursor to the documents.
        :rtype: cursor
        """
        # create the index
        self.db.create_index([("post_body", "text")])
        posts = self.db.find({"$text": {"$search": query}})

        return posts
