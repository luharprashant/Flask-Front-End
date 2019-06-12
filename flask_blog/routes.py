import secrets
from flask import render_template, url_for, flash, redirect, request
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, VideoUploadForm
from flask_blog.models import User, Videos
from flask_blog import app, db, bcrypt
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
import os

videos = []

@app.route("/")
@app.route("/home")
def home():
	if current_user.is_authenticated:
		return render_template('home.html',title='About')
	else:
		return redirect(url_for('login'))
		

@app.route("/about")
def about():
	if current_user.is_authenticated:
		return render_template('about.html',title='About')
	else:
		return redirect(url_for('login'))

@app.route("/register",methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hash_pw)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created!','success')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash(f'You have been logged in!', 'success')
			return redirect(url_for('home')) 
		else:
			flash(f'Login Unsuccessful. Please check email and password','danger')
	return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile/', picture_fn)
	form_picture.save(picture_path)
	return picture_fn

@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash(f'Your account has been updated','successs')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.email.data = current_user.email
		form.username.data = current_user.username
	image = url_for('static',filename='profile/' + current_user.image)
	return render_template('account.html',title='Account',image=image,form=form)

def process_video(process_video):
	# actual processig of the video i.e. analytics code using the model 
	process = 'Okay'
	return process

@app.route("/upload", methods=["GET", "POST"])
def upload():
	form = VideoUploadForm()
	if form.validate_on_submit():
		string = process_video(form.video.data)
		print(string)
	return render_template('video_upload.html',title='Video Upload',form=form)