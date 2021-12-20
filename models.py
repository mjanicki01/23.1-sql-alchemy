from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    img_url = db.Column(db.String, nullable=False, default="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png")


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
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('Users', backref='posts')