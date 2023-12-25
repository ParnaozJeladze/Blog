from flask import render_template, redirect
from flask_login import login_user, logout_user, current_user
from forms import AddBlogForm, RegisterForm, LoginForm,  EditBlogForm
from models import Blog, User
from ext import app, db
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures.file_storage import FileStorage


@app.route("/")
def web():
    blogs = Blog.query.all()
    return render_template("blogs.html", blogs=blogs)

@app.route("/home")
def home():
    latest_blogs = Blog.query.order_by(Blog.id.desc()).limit(2).all()
    return render_template("home.html", latest_blogs=latest_blogs)


@app.route("/addblog", methods=["GET", "POST"])
def add_blog():
    form = AddBlogForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        img = form.img.data
        if img:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_blog = Blog(title=title, content=content, img=filename, user=current_user.username)
            db.session.add(new_blog)
            db.session.commit()
        else:
            new_blog = Blog(title=title, content=content, user=current_user.username)
            db.session.add(new_blog)
            db.session.commit()
        return redirect("/")
    return render_template("addblog.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/edit_blog/<int:index>", methods=["GET", "POST"])
def edit_blog(index):
    blog = Blog.query.get(index)
    if current_user.username == blog.user or current_user.username == "Admin":
        form = EditBlogForm(title=blog.title, content=blog.content, img=blog.img)
        if form.validate_on_submit():
            blog.title = form.title.data
            blog.content = form.content.data
            img = form.img.data
            if type(img) == FileStorage:
                filename = secure_filename(img.filename)
                img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                blog.img = filename

            db.session.commit()
            return redirect("/")
    return render_template("addblog.html", form=form)


@app.route("/delete_blog/<int:index>", methods=["GET", "POST"])
def delete_blog(index):
    blog = Blog.query.get(index)
    if current_user.username == blog.user or current_user.username == "Admin":
        db.session.delete(blog)
        db.session.commit()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data, password=form.password.data).first()
        if user:
            login_user(user)
            return redirect('/')
        else:
            return render_template("login.html", form=form, errors=["incorrect password or email"])

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter_by(username=form.email.data).first()
        if user_in_db:
            return render_template("register.html", form=form, db_errors=["User already excisted"])
        user = User(username=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")
# title="Reset Request",
# @app.route("/search/<string:name>")
# def search(name):
#     blog = Blog.query.filter()
#     return render_template("about.html")
# @app.route("/reset_password", methods=["GET", "POST"])
# def reset_request():
#     form = ResetRequestForm()
#     if form.validate_on_submit():
#         print("Reset request sent. Check your mail.", "success")
#     return render_template("reset_request.html",  form=form)
