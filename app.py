from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts, Tags, PostsTags

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



# User-specific routes & view functions -------------------------------------------------------

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
    new_user  = Users(
    first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    img_url = request.form["image"] or None)

    db.session.add(new_user)
    db.session.commit()

    flash("New user added", "success")
    return redirect('/')


@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    Users.query.filter(Users.id == user_id).delete()
    db.session.commit()

    flash("User deleted", "success")
    return redirect('/')


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

    flash("User updated", "success")
    return redirect('/')



# Post-specific routes & view functions ------------------------------------------

@app.route('/posts')
def list_posts():
    posts = Posts.query.all()

    return render_template('indexposts.html', posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = Posts.query.get_or_404(post_id)
    tags = db.session.query(Tags.name, PostsTags.tag_id, PostsTags.post_id).join(PostsTags).filter(PostsTags.post_id == post_id).all()

    return render_template("postdetail.html", post=post, tags=tags)


@app.route('/addpost/<int:user_id>')
def render_add_post(user_id):
    user = Users.query.get_or_404(user_id)
    tags = Tags.query.all()

    return render_template('addpost.html', user=user, tags=tags)


@app.route('/addpost', methods=["POST"])
def add_post():
    title = request.form["title"]
    content = request.form["content"]
    creator_id = request.form["creator_id"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tags.query.filter(Tags.id.in_(tag_ids)).all()
    new_post  = Posts(title=title, content=content, creator_id=creator_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash("New post added", "success")
    return redirect(f'/{creator_id}')


@app.route("/delete/post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    Posts.query.filter(Posts.id == post_id).delete()
    db.session.commit()

    flash("Post deleted", "success")
    return redirect('/')


@app.route('/updatepost/<int:post_id>')
def render_update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    tags = Tags.query.all()

    return render_template('updatepost.html', post=post, tags=tags)


@app.route('/updatepost/<int:post_id>', methods=["POST"])
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)

    if request.form["title"]:
        post.title = request.form["title"]
        flash("Post title updated", "success")

    if request.form["content"]:
        post.content = request.form["content"]
        flash("Post content updated", "success")

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tags.query.filter(Tags.id.in_(tag_ids)).all()
    
    post.creator_id = request.form["creator_id"]

    db.session.add(post)
    db.session.commit()


    return redirect(f'/post/{post_id}')




# Tag-specific routes & view functions ---------------------------------------------------

@app.route('/tag')
def list_tags():
    tags = Tags.query.all()

    return render_template('indextags.html', tags=tags)


@app.route("/tag/<int:tag_id>")
def show_tag(tag_id):
    tag = Tags.query.get_or_404(tag_id)
    posts = db.session.query(Posts.title, PostsTags.tag_id, PostsTags.post_id).join(PostsTags).filter(PostsTags.tag_id == tag_id).all()
    return render_template("tagdetail.html", tag=tag, posts=posts)


@app.route('/addtag')
def render_add_tag():

    return render_template('addtag.html')


@app.route('/addtag', methods=["POST"])
def add_tag():
    new_tag  = Tags(name = request.form["name"])

    db.session.add(new_tag)
    db.session.commit()

    flash("New tag added", "success")
    return redirect('/tag')


@app.route("/delete/tag/<int:tag_id>", methods=["POST"])
def delete_tag(tag_id):
    Tags.query.filter(Tags.id == tag_id).delete()
    db.session.commit()

    flash("Tag deleted", "success")
    return redirect('/')


@app.route('/updatetag/<int:tag_id>')
def render_update_tag(tag_id):
    tag = Tags.query.get_or_404(tag_id)

    return render_template('updatetag.html', tag=tag)


@app.route('/updatetag/<int:tag_id>', methods=["POST"])
def update_tag(tag_id):
    tag = Tags.query.get_or_404(tag_id)
    if request.form["name"]:
        tag.name = request.form["name"]
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag renamed: {tag.name}", "success")

    return redirect(f'/tag/{tag_id}')