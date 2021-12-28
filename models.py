from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"

def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    img_url = db.Column(db.String, nullable=False, default=DEFAULT_IMG_URL)

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.img_url} >"


class Posts(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                    nullable=False)
    content = db.Column(db.String(500),
                    nullable=False)
    created_at = db.Column(db.DateTime,
                    default=db.func.current_timestamp())
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"),
                    nullable=False)

    creator = db.relationship('Users', backref='posts')
    tagged_posts = db.relationship('Tags', secondary="posts_tags", backref='posts', viewonly=True)

    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.content} {self.created_at} {self.creator_id} >"


class Tags(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(15),
                    nullable=False, unique=True)

    tagged_posts = db.relationship('Posts', secondary="posts_tags", backref='tags', viewonly=True)

    def __repr__(self):
        return f"<Tag {self.id} {self.name} >"


class PostsTags(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"),
                    primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"),
                    primary_key=True)

    def __repr__(self):
        return f"<PT Post_id: {self.post_id} Tag_id: {self.tag_id} >"