from crypt import methods
from email.mime import image
from re import L
import flask
from urllib import response
from flask import Flask, jsonify, request, render_template,  redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from matplotlib import artist
from numpy import choose
from models import db,  connect_db, User, Post,Likes,Inspiration
from sqlalchemy.exc import IntegrityError,InvalidRequestError
from form import UserAddForm, LoginForm, UserEditForm, PostForm,EditPostForm,choices
import json
import requests
from random import sample
from sqlalchemy import func, null
CURR_USER_KEY = "curr_user"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)
with app.app_context(): 
    db.create_all()
##############################################################################
# search without js
search_base_api = "https://collectionapi.metmuseum.org/public/collection/v1/search?"
objectIDs_api="https://collectionapi.metmuseum.org/public/collection/v1/objects/"
@app.route('/')
def homepage():
    """Show homepage:"""
    res = requests.get(f"{search_base_api}",params={"q":"image", "hasImages": "true"})
    five_random = sample(list(res.json()['objectIDs']), 5)
    img_urls={}
    for rand in range(len(five_random)):
        object_res = requests.get(f"{objectIDs_api}{five_random[rand]}")
        object_data=object_res.json()
        image= object_data.get("primaryImage")
        artist= object_data.get("artistDisplayName")
        if image:
            img_urls[artist] = image         
    return render_template('home/home.html' , img_urls = img_urls, choices=choices)
@app.route('/five-api')
def home_api():
    """Show homepage:"""
    img_urls=[]
    res = requests.get(f"{search_base_api}",params={"q":"image", "hasImages": "true"}) 
    five_random = sample(list(res.json()['objectIDs']), 7) 
    for rand in range(len(five_random)):
        object_res = requests.get(f"{objectIDs_api}{five_random[rand]}")
        img_urls.append(object_res.json())
    return img_urls
############################################################################## query search
@app.route('/searched', methods=["GET", "POST"])
def search():
    """Show homepage:"""
    search = request.args.get('image')
    res = requests.get(f"{search_base_api}hasImages=true&q={search}")
    ten_random = sample(list(res.json()['objectIDs']), 10)
    inspirations = (Inspiration.query
                .order_by(Inspiration.id.desc())
                .limit(15)
                .all())
    return render_template('home/search.html',img_ids=ten_random, inspirations=inspirations)
##############################################################################
# search by department 
@app.route('/by-department', methods=["GET"])
def by_department():
    """Show search by department"""
    departmentId = request.args.get('departmentIds')
    department_name=choices.get(int(departmentId))
    res = requests.get(f"{search_base_api}departmentId={departmentId}&q=image")
    print(department_name)
    ten_random = sample(list(res.json()['objectIDs']), 10)
    inspirations = (Inspiration.query
                    .order_by(Inspiration.id.desc())
                    .limit(15)
                    .all())
        
    return render_template('home/by-department.html',img_ids=ten_random, inspirations=inspirations, department_name=department_name, choices=choices)
#############################################################################
# User signup/login/logout
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None
# I do not understand flask global all to well
def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id
def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message and re-present form.
    """
    form = UserAddForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                avatar=form.avatar.data or User.avatar.default.arg)
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
        do_login(user)
        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        flash("Invalid credentials.", 'danger')
    return render_template('users/login.html', form=form)
@app.route('/logout')
def logout():
    """Handle logout of user."""
    session.pop(CURR_USER_KEY)
    # or do_logout()
    flash("Goodbye!", "info")
    return redirect('/login')
##############################################################################
# list user's post:
@app.route('/post/new', methods=["GET", "POST"])
def post_add():
    """Add a post:
    Show form if GET. If valid, update message and redirect to user page.
    """
    if not g.user:
        flash("Please sign up first : }", "info")
        return redirect("/")
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, 
                    description=form.description.data,
                    imageURL=form.imageURL.data)
        g.user.posts.append(post)
        db.session.commit()
        return redirect(f"/users/{g.user.id}")
    return render_template('posts/addpost.html', form=form)
@app.route('/post/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Add a post:
    Show form if GET. If valid, update post and redirect to user page.
    """
    posts = Post.query.get_or_404(post_id)
    if not g.user:
        flash("Please sign up first : }", "info")
        return redirect("/")
    form = EditPostForm(obj=posts)
    if form.validate_on_submit():
        posts.title=form.title.data, 
        posts.description=form.description.data,
        posts.imageURL=form.imageURL.data
        db.session.commit()
        return redirect(f"/users/{g.user.id}")
    return render_template('posts/edit.html', form=form, posts=posts)
@app.route('/post/<int:post_id>/delete', methods=["POST"])
def messages_destroy(post_id):
    """Delete a message."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{g.user.id}")
##############################################################################
#  users pofile:
@app.route('/users/<int:user_id>', methods=["GET"])
def show_user_info(user_id):
    """Show user profile and posts."""
    user = User.query.get_or_404(user_id)
    if g.user:
        post = (Post
                    .query
                    .filter(Post.user_id==user_id)
                    .order_by(Post.created_at.desc())
                    .limit(15)
                    .all())
        
        likes=[post.id for post in g.user.likes]
        return render_template('users/show.html', post=post, user=user, likes=likes)
    else:
        return render_template('home/home-anon.html')
@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user=g.user
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        if User.authenticate(user.username,form.password.data):
            user.email=form.email.data
            user.avatar=form.avatar.data or User.image_url.default.arg
            user.bio=form.bio.data
            user.social_media=form.social_media.data
            db.session.commit()
            return redirect(f"/users/{user.id}")
        flash("Wrong Password, please try again.", "danger")
    else:
        return render_template('users/edit.html', form=form, user=user)
@app.route("/user/<int:user_id>/profile")
def post_user_info(user_id):
    """show post and info about user"""
    user=User.query.get_or_404(user_id)
        
    return render_template('posts/user_info.html', user=user)
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    do_logout()
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/signup")
##############################################################################
# list shared posts:
@app.route("/posts")
def users_post():
    """how list of users post"""
    posts = (Post.query
                .order_by(Post.created_at.desc())
                .limit(15)
                .all())
        
    liked_post_id=[post.id for post in g.user.likes]
    likes_on_post= (Likes
                    .query.filter(Likes.user_id==g.user.id).all()
        )
    return render_template('posts/show.html', posts=posts, likes=liked_post_id, likes_on_post=likes_on_post)
@app.route("/posts/<int:post_id>/like",methods=["POST"] )
def like_a_post(post_id):
    """toggle like"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
        
    liked_post= Post.query.get_or_404(post_id)
    user_likes= g.user.likes
    if liked_post in user_likes:
        g.user.likes= [ like for like in user_likes if like!=liked_post]
    else:
        g.user.likes.append(liked_post)
    db.session.commit()
    return redirect("/posts")
@app.route('/users/<int:user_id>/likes', methods=["GET"])
def show_user_likes(user_id):
    """Show user likes"""
    if g.user:
        post = (Post
                    .query
                    .filter(Post.user_id==user_id)
                    .order_by(Post.created_at.desc())
                    .limit(15)
                    .all())
        likes=[post for post in g.user.likes]
        return render_template('users/likes.html', post=post, likes=likes)
##############################################################################
# Save liked art from MET API and list them 
@app.route("/inspiration/<int:objectID>/add", methods=["GET", "POST"] )
def like_an_art(objectID):
    """toggle liked Art. Add an artwork to your list for    later inspiration:
#     """
    if not g.user:
        flash("Access unauthorized.Signup or login first", "danger")
        return redirect("/")
    if objectID not in g.user.inspiration:
        inspiration = Inspiration(inspiration=objectID, user_id=g.user.id)
        db.session.add(inspiration)
        db.session.commit()
    return redirect(f"/users/{g.user.id}/saves")
@app.route('/users/<int:user_id>/saves', methods=["GET"])
def show_user_saves(user_id):
    """Show user liked """
    if g.user:
        arts = (Inspiration
                    .query
                    .filter(Inspiration.user_id==user_id)
                    .order_by(Inspiration.id.desc())
                    .limit(20)
                    .all())
        return render_template('METArt/art-saves.html', arts=arts)
@app.route('/inspiration/<int:inspiration_id>/remove', methods=["POST"])
def delete_inspiration(inspiration_id):
    """Delete user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    inspiration=Inspiration.query.get_or_404(inspiration_id)
    db.session.delete(inspiration)
    db.session.commit()
    return redirect(f"/users/{g.user.id}/saves")