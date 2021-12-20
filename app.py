from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "db3NJS8"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def list_users():
    users = Users.query.all()

    return render_template('index.html', users=users)


# User-specific routes & view functions ------------------

@app.route("/<int:user_id>")
def user_detail(user_id):
    user = Users.query.get_or_404(user_id)
    posts = Posts.query.filter_by(creator_id = user_id)

    return render_template("userdetail.html", user=user, posts=posts)


@app.route('/adduser')
def render_add_user():

    return render_template('adduser.html')


@app.route('/adduser', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["image"]
    new_user  = Users(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')


@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    Users.query.filter(Users.id == user_id).delete()
    db.session.commit()

    return redirect('/')
#to-do: Create method in models.py to handle try/except to handle if user has posts (fk constraint violation)


@app.route("/update/<int:user_id>")
def render_update_user(user_id):
    user = Users.query.get_or_404(user_id)

    return render_template('updateuser.html', user=user)


@app.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
    user = Users.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect('/')



# Post-specific routes & view functions ---------------------

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = Posts.query.get_or_404(post_id)

    return render_template("postdetail.html", post=post)


@app.route('/addpost/<int:user_id>')
def render_add_post(user_id):
    user = Users.query.get_or_404(user_id)

    return render_template('addpost.html', user=user)


@app.route('/addpost', methods=["POST"])
def add_post():
    title = request.form["title"]
    content = request.form["content"]
    creator_id = request.form["creator_id"]
    new_post  = Posts(title=title, content=content, creator_id=creator_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{creator_id}')


@app.route("/delete/post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    Posts.query.filter(Posts.id == post_id).delete()
    db.session.commit()

    return redirect('/')


@app.route('/updatepost/<int:post_id>')
def render_update_post(post_id):
    post = Posts.query.get_or_404(post_id)

    return render_template('updatepost.html', post=post)


@app.route('/updatepost/<int:post_id>', methods=["POST"])
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.creator_id = request.form["creator_id"]

    db.session.add(post)
    db.session.commit()

    return redirect(f'/post/{post_id}')