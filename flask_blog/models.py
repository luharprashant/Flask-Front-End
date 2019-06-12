from datetime import datetime
from flask_blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	videos = db.relationship('Videos', backref='uploader', lazy=True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image}')"

class Videos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.now())
	player = db.Column(db.String(40), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Videos('{self.title}','{self.date}')"
