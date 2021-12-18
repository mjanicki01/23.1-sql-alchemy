from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "db3NJS8"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
#db.create_all()

@app.route('/')
def list_users():
    users = Users.query.all()
    return render_template('index.html', users=users)


@app.route('/adduser')
def render_add_user():
    return render_template('adduser.html')


@app.route('/adduser', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["image"]
    new_user  = Users(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')


@app.route("/<int:user_id>")
def show_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template("userdetail.html", user=user)


@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    Users.query.filter(Users.id == user_id).delete()
    db.session.commit()
    return redirect('/')


@app.route("/update/<int:user_id>")
def render_update_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('updateuser.html', user=user)


@app.route("/update/<int:user_id>", methods=["POST"])
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect('/')

