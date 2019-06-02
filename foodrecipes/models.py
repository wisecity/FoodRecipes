from datetime import datetime
from foodrecipes import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)


class Recipe(db.Model):
	__tablename__ = 'recipe'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	duration = db.Column(db.Integer)
	content = db.Column(db.Text, nullable=False)
	view_count = db.Column(db.Integer)
	like_count = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Ingredients(db.Model):
	__tablename__ = 'ingredients'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	price = db.Column(db.Integer)


'''
class RecipeIngredientsAssoc(db.Model):
	__tablename__ = 'recipe_ingredients_assoc'
	id = db.Column(db.Integer, primary_key=True)
	quantity = db.Column(db.Integer)
	recipe_id = db.Column(db.Integer, nullable=False, db.ForeignKey('recipe.id'))
	ingredients_id = db.Column(db.Integer, nullable=False, db.ForeignKey('ingredients.id'))
'''
