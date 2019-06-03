from datetime import datetime
from foodrecipes import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	__tablename__ = 'USER'
	Id = db.Column(db.Integer, primary_key=True)
	Username = db.Column(db.String(60), unique=True, nullable=False)
	Password = db.Column(db.String(60), nullable=False)


class Recipe(db.Model):
	__tablename__ = 'RECIPE'
	Id = db.Column(db.Integer, primary_key=True) 
	Name = db.Column(db.String(100), nullable=False)
	PostTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	Contents = db.Column(db.Text)
	Views = db.Column(db.Integer)
	Score = db.Column(db.Float)
	Uid = db.Column(db.Integer, db.ForeignKey('USER.Id'), nullable=False)

