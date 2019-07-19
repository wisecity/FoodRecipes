from datetime import datetime
from run import login_manager, db
from flask_appbuilder.models.mixins import ImageColumn

class Ingredient_Photos(db.Model):
	__tablename__ = 'INGREDIENT_PHOTOS'
	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
	photo_link = db.Column(db.String)

	def __init__(self, recipe_id, photo_link):
		self.recipe_id = recipe_id
		self.photo_link = photo_link

	def json(self):
		return {'id': self.id, 'recipe_id' : self.recipe_id}

	@classmethod

	def delete_photo(self, name, username):
		_user = User.query.filter_by(username=username).first()
		_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
		Ingredient_Photos.query.filter_by(recipe_id = _recipe.id, id = self.id).delete()
		db.session.commit()

	def get_photos(recipe_id):
		photoList = Ingredient_Photos.query.filter_by(recipe_id = recipe_id).all()
		return photoList

	def create_to(self):
		db.session.add(self)
		db.session.commit()


class Step_Photos(db.Model):
	__tablename__ = 'STEP_PHOTOS'
	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
	photo_link = db.Column(db.String)

	def __init__(self, recipe_id, photo_link):
		self.recipe_id = recipe_id
		self.photo_link = photo_link

	def json(self):
		return {'id': self.id, 'recipe_id' : self.recipe_id}

	@classmethod

	def delete_photo(self, name, username):
		_user = User.query.filter_by(username=username).first()
		_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
		Step_Photos.query.filter_by(recipe_id = _recipe.id, id = self.id).delete()
		db.session.commit()

	def get_photos(recipe_id):
		photoList = Step_Photos.query.filter_by(recipe_id = recipe_id).all()
		return photoList

	def create_to(self):
		db.session.add(self)
		db.session.commit()

class Final_Photos(db.Model):
	__tablename__ = 'FINAL_PHOTOS'
	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
	photo_link = db.Column(db.String)

	def __init__(self, recipe_id, photo_link):
		self.recipe_id = recipe_id
		self.photo_link = photo_link

	def json(self):
		return {'id': self.id, 'recipe_id' : self.recipe_id}

	@classmethod

	def delete_photo(self, name, username):
		_user = User.query.filter_by(username=username).first()
		_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
		Final_Photos.query.filter_by(recipe_id = _recipe.id, id = self.id).delete()
		db.session.commit()

	def get_photos(recipe_id):
		photoList = Final_Photos.query.filter_by(recipe_id = recipe_id).all()
		return photoList

	def create_to(self):
		db.session.add(self)
		db.session.commit()

class Tags(db.Model):
		__tablename__ = 'TAGS'
		id = db.Column(db.Integer, primary_key=True)
		recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
		name = db.Column(db.String(32))

		def __init__(self, recipe_id, name):
			self.recipe_id = recipe_id
			self.name = name

		def json(self):
			return {'id': self.id, 'recipe_id' : self.recipe_id, 'name': self.name}


		@classmethod
		def find_by_recipe_id(self, recipe_id):
			tags = self.query.filter_by(recipe_id=recipe_id).all()
			tags_str = ''
			for tag in tags:
				tags_str += tag.name
				tags_str += "-"
			tags_str = tags_str[:-1]
			return tags_str


		def add_tag(self):
			db.session.add(self)
			db.session.commit()
			return self.id


		def get_tags(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			tagList = Tags.query.filter_by(recipe_id = _recipe.id).all()
			return tagList

class User(db.Model):
	__tablename__ = 'USER'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)


	def __init__(self, username, password):
		self.username = username
		self.password = password

	def json(self):
		return {'User name': self.username, "id" : self.id}

	@staticmethod
	def find_by_id(id):
		return User.query.filter_by(id=id).first()

	@staticmethod
	def find_by_username(username):
		return User.query.filter_by(username=username).first()

	def delete_by_id(id):
		User.query.filter_by(id=id).delete()
		db.session.commit()

	def delete_by_username(username):
		User.query.filter_by(username=username).delete()
		db.session.commit()

	def add_user(self):
		db.session.add(self)
		db.session.commit()
		return self.id

	def update_user(self):
		_user = User.query.filter_by(id=self.id).first()
		_user.username = self.username
		_user.password = self.password
		db.session.commit()
		return self.id

	def get_recipe_list(self):
		_user = User.query.filter_by(id=self.id).first()
		recipeList = Recipe.query.filter_by(user_id = _user.id).all()
		return recipeList


class Recipe(db.Model):
	__tablename__ = 'RECIPE'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	post_time = db.Column(db.String(100))
	contents = db.Column(db.Text)
	details = db.Column(db.Text)
	views = db.Column(db.Integer, default=0)
	likes = db.Column(db.Integer, default=0)
	user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, default=0)

	def __init__(self, name, contents, details, post_time=None, views=None, likes=None, user_id=None):
		self.name = name
		self.contents = contents
		self.details = details

		if post_time != None:
			self.post_time = post_time
		if views != None:
			self.views = views
		if likes != None:
			self.likes = likes
		if user_id != None:
			self.user_id = user_id


	def json(self):
		return {'name': self.name, "post_time" : str(self.post_time), "contents" : self.contents, "details" : self.details, "views" : self.views, "likes" : self.likes, "user_id" : self.user_id}

	@staticmethod
	def find_by_id(id):
		return Recipe.query.filter_by(id=id).first()


	@staticmethod
	def find_by_name(name):
		return Recipe.query.filter_by(name=name).all()


	@staticmethod
	def find_by_username(username):
		print(type(Recipe.query.all()))
		user = User.query.filter_by(username=username).first()
		if user == None:
			return []
		else:
			return Recipe.query.filter_by(user_id=user.id).all()


	@staticmethod
	def find_by_tag_name(tag_name):
		tags = Tags.query.filter_by(name=tag_name).all()
		tag_id_list = []
		for tag in tags:
			if tag.recipe_id not in tag_id_list:
				tag_id_list.append(tag.recipe_id)

		return [Recipe.query.filter_by(id=tag_id).first() for tag_id in tag_id_list]



	@staticmethod
	def find_by_details(details):
		return Recipe.query.filter_by(details=details).all()


	@staticmethod
	def find_by_contents(contents):
		return Recipe.query.filter_by(contents=contents).all()


	def get_liked_posts(user_id):
		ids = Like.get_liked_by_user_id(user_id)


	def delete_by_id(id):
		Recipe.query.filter_by(id=id).delete()
		db.session.commit()


	def add_recipe(self):
		db.session.add(self)
		db.session.commit()
		print("Recipe Self-id: ", self.id)
		return self.id


	def update_recipe(self):
		_recipe = Recipe.query.filter_by(id=self.id).first()
		_recipe.name = self.name
		_recipe.post_time = self.post_time
		_recipe.contents = self.contents
		_recipe.details = self.details
		_recipe.views = self.views
		_recipe.likes = self.likes
		_recipe.user_id = self.user_id
		db.session.commit()


	def delete_recipe(self, username):
		_user = User.query.filter_by(username=username).first()
		Recipe.query.filter_by(user_id = _user.id, id = self.id).delete()
		db.session.commit()

	def delete_tags(self):
		Tags.query.filter_by(recipe_id=self.id).delete()
		db.session.commit()

	def increase_view(self):
		self.views = self.views + 1
		db.session.commit()

	def increase_like(self):
		self.likes = self.likes + 1
		db.session.commit()

db.create_all()
