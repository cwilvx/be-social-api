from . import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    post_owner = db.Column(db.String)
    post_title = db.Column(db.String)
    post_body = db.Column(db.String)

    # @property
    def __repr__(self):
        return f'Post {self.post_title}'

    # def publish_post(self):
    #     db.session.add(self)
    #     db.session.commit()
