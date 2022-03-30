"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET123!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_root():
    """Homepage redirects to users page"""

    return redirect("/users")

@app.route("/users")
def show_users():
    """Show all users."""

    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def new_user():
    """Show new user form"""

    return render_template("new_user_form.html")

@app.route("/users/new", methods=['POST'])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name, 
                    last_name=last_name, 
                    image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user details"""
    
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show user edit form"""
    
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=['POST'])
def update_user(user_id):
    """Edit user"""
    user = User.query.get_or_404(user_id)
    if request.form['first_name']:
        user.first_name = request.form['first_name']
    if request.form['last_name']:
        user.last_name = request.form['last_name']
    if request.form['image_url']:
        user.image_url = request.form['image_url'] 

    db.session.add(user)
    db.session.commit()

    return redirect('/')


@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")
