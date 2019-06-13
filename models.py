from datetime import datetime
from run import login_manager, db


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

	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id=id).first()

	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	def create_to(self):
		db.session.add(self)
		db.session.commit()

	def delete_by_id(cls, id):
		cls.query.filter_by(id=id).delete()
		db.session.commit()

	def delete_by_username(cls, username):
		cls.query.filter_by(username=username).delete()
		db.session.commit()

	def update_(self, cls):
		_user = cls.query.filter_by(id=self.id).first()
		_user.username = self.username
		_user.password = self.password
		db.session.commit()

	def get_recipe_list(self):
		_user = User.query.filter_by(id=self.id).first()
		recipeList = Recipe.query.filter_by(user_id = _user.id).all()
		return recipeList


class Recipe(db.Model):
	__tablename__ = 'RECIPE'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	post_time = db.Column(db.DateTime, default=datetime.utcnow)
	contents = db.Column(db.Text)
	details = db.Column(db.Text)
	views = db.Column(db.Integer, default=0)
	score = db.Column(db.Float, default=0.0)
	user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, default=0)

	def __init__(self, name, contents, details, post_time=None, views=None, score=None, user_id=None):
		self.name = name
		self.contents = contents
		self.details = details

		if post_time != None:
			self.post_time = post_time
		if views != None:
			self.views = views
		if score != None:
			self.score = score    
		if user_id != None:
			self.user_id = user_id            	


	def json(self):
		return {'name': self.name, "post_time" : str(self.post_time), "contents" : self.contents, "details" : self.details, "views" : self.views, "score" : self.score, "user_id" : self.user_id}

	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id=id).first()

	def find_by_name(cls, recipename):
		return cls.query.filter_by(name=recipename).first()

	def create_to(self):
		db.session.add(self)
		db.session.commit()

	def delete_by_id(cls, id):
		cls.query.filter_by(id=id).delete()
		db.session.commit()

	def delete_by_name(cls, name):
		cls.query.filter_by(name=name).delete()
		db.session.commit()

	def update_(self, cls):
		_recipe = cls.query.filter_by(id=self.id).first()
		_recipe.name = self.name
		_recipe.post_time = self.post_time
		_recipe.contents = self.contents
		_recipe.details = self.details
		_recipe.views = self.views
		_recipe.score = self.score
		_recipe.user_id = self.user_id
		db.session.commit()

	def add_recipe(self, username):
		_user = User.query.filter_by(username=username).first()
		# Hack here.
		if _user == None:
			self.user_id = 0
		else:
			self.user_id = _user.id
		db.session.add(self)
		db.session.commit()

	def delete_recipe(self, username):
		_user = User.query.filter_by(username=username).first()
		Recipe.query.filter_by(user_id = _user.id, id = self.id).delete()
		db.session.commit()

	def edit_recipe(self, username):
		_user = User.query.filter_by(username=username).first()
		_recipe = Recipe.query.filter_by(user_id = _user.id, id = self.id)
		_recipe.name = self.name
		_recipe.post_time = self.post_time
		_recipe.contents = self.contents
		_recipe.details = self.details
		_recipe.views = self.views
		_recipe.score = self.score
		_recipe.user_id = self.user_id
		db.session.commit()

	def increase_view(self):
		self.views = self.views + 1
		db.session.commit()


	class Ingredient_Photos(db.Model):
		__tablename__ = 'INGREDIENT_PHOTOS'
		id = db.Column(db.Integer, primary_key=True)
		recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
		photo_location = db.Column(db.String(100))

		def __init__(self, recipe_id, photo_location):
			self.recipe_id = recipe_id
			self.photo_location = photo_location
		
		def json(self):
			return {'id': self.id, 'recipe_id' : self.recipe_id, 'photo_location': self.photo_location}

		@classmethod
		def add_photo(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			self.recipe_id = _recipe.id
			db.session.add(self)
			db.session.commit()

		def delete_photo(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			Ingredient_Photos.query.filter_by(recipe_id = _recipe.id, id = self.id).delete()
			db.session.commit()

		def get_photos(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			photoList = Ingredient_Photos.query.filter_by(recipe_id = _recipe.id).all()
			return photoList


	class Step_Photos(db.Model):
		__tablename__ = 'STEP_PHOTOS'
		id = db.Column(db.Integer, primary_key=True)
		recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
		photo_location = db.Column(db.String(100))

		def __init__(self, recipe_id, photo_location):
			self.recipe_id = recipe_id
			self.photo_location = photo_location

		def json(self):
			return {'id': self.id, 'recipe_id' : self.recipe_id, 'photo_location': self.photo_location}

		@classmethod
		def add_photo(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			self.recipe_id = _recipe.id
			db.session.add(self)
			db.session.commit()

		def delete_photo(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			Step_Photos.query.filter_by(recipe_id = _recipe.id, id = self.id).delete()
			db.session.commit()
		
		def get_photos(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			photoList = Step_Photos.query.filter_by(recipe_id = _recipe.id).all()
			return photoList


	class Final_Photos(db.Model):
		__tablename__ = 'FINAL_PHOTOS'
		id = db.Column(db.Integer, primary_key=True)
		recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
		photo_location = db.Column(db.String(100))

		def __init__(self, recipe_id, photo_location):
			self.recipe_id = recipe_id
			self.photo_location = photo_location

		def json(self):
			return {'id': self.id, 'recipe_id' : self.recipe_id, 'photo_location': self.photo_location}

		@classmethod
		def add_photo(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			self.recipe_id = _recipe.id
			db.session.add(self)
			db.session.commit()

		def delete_photo(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			Final_Photos.query.filter_by(recipe_id = _recipe.id, id = self.id).delete()
			db.session.commit()

		def get_photos(self, name, username):
			_user = User.query.filter_by(username=username).first()
			_recipe = Recipe.query.filter_by(user_id = _user.id, name=name)
			photoList = Final_Photos.query.filter_by(recipe_id = _recipe.id).all()
			return photoList
