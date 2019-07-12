from datetime import datetime
from run import login_manager, db
from flask_appbuilder.models.mixins import ImageColumn

class Ingredient_Photos(db.Model):
	__tablename__ = 'INGREDIENT_PHOTOS'
	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
	photo = db.Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))

	# photo_location yerine photo_phase desek?
	def __init__(self, recipe_id, photo_location):
		self.recipe_id = recipe_id
		self.photo_location = photo_location
	
	def json(self):
		return {'id': self.id, 'recipe_id' : self.recipe_id}

	'''
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
	'''
	def add_photo(self):
		db.session.add(self)
		db.session.commit()
		return self.id


	def delete_photo(self):
		deleted_id = self.id
		Ingredient_Photos.query.filter_by(id = self.id).delete()
		db.session.commit()		
		return deleted_id


	def get_photos(self):
		photoList = Ingredient_Photos.query.filter_by(recipe_id=self.recipe_id).all()
		return photoList		


class Step_Photos(db.Model):
	__tablename__ = 'STEP_PHOTOS'
	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
	photo = db.Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))

	# photo_location yerine photo_phase desek?
	def __init__(self, recipe_id, photo_location):
		self.recipe_id = recipe_id
		self.photo_location = self.photo_location


	def json(self):
		return {'id': self.id, 'recipe_id' : self.recipe_id,}


	@classmethod
	def add_photo(self, recipe_id):
		self.recipe_id = recipe_id
		db.session.add(self)
		db.session.commit()
		return self.id


	def delete_photo(self):
		deleted_photo_id = self.id
		Step_Photos.query.filter_by(id=self.id).delete()
		db.session.commit()
		return delete_photo_id
	

	def get_photos(self, recipe_id):
		photoList = Step_Photos.query.filter_by(recipe_id=recipe_id).all()
		return photoList


class Final_Photos(db.Model):
	__tablename__ = 'FINAL_PHOTOS'
	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
	photo = db.Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))


	def __init__(self, recipe_id, photo_location):
		self.recipe_id = recipe_id
		self.photo_location = photo_location


	def json(self):
		return {'id': self.id, 'recipe_id' : self.recipe_id}


	@classmethod
	def add_photo(self, recipe_id):
		self.recipe_id = recipe_id
		db.session.add(self)
		db.session.commit()
		return self.id


	def delete_photo(self):
		deleted_photo_id = self.id
		Final_Photos.query.filter_by(id=self.id).delete()
		db.session.commit()
		return delete_photo_id


	def get_photos(self, recipe_id):
		photoList = Final_Photos.query.filter_by(recipe_id=recipe_id).all()
		return photoList


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


		def delete_tag(self, recipe_id, tag_name):
			deleted_tag_id = self.id
			Tags.query.filter_by(recipe_id=_recipe.id, name=tag_name).delete()
			db.session.commit()
			return deleted_tag_id


		def get_tags(self, recipe_id):
			tagList = Tags.query.filter_by(recipe_id=recipe_id).all()
			return tagList



class Like(db.Model):
	__tablename__ = 'LIKE'
	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('RECIPE.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False)


	def __init__(self, recipe_id, user_id):
		self.recipe_id = recipe_id
		self.user_id = user_id


	def add_like(self):
		db.session.add(self)
		db.session.commit()
		return self.id


	def delete_like(self, recipe_id, user_id):
		deleted_like_id = self.id
		Like.query.filter_by(recipe_id=recipe_id, user_id=user_id).delete()
		db.session.commit()
		return deleted_like_id


	# Helper to get_liked_posts()
	# returns liked recipe's id
	@staticmethod
	def get_liked_by_user_id(user_id):
		user = User.query.filter_by(user_id).first()
		likes = Like.query.filter_by(user_id=user.id).all()
		liked_posts_id = []
		for like_item in likes:
			liked_posts_id.append(like_item.recipe_id)
		return liked_posts_id


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


	@staticmethod
	def delete_by_id(id):
		User.query.filter_by(id=id).delete()
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
		recipeList = Recipe.query.filter_by(user_id=_user.id).all()
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
		return {'id': self.id, 'name': self.name, "post_time" : str(self.post_time), "contents" : self.contents, "details" : self.details, "views" : self.views, "score" : self.score, "user_id" : self.user_id}


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
		tags = Tags.query.filter_by(name).all()
		tag_id_list = []
		for tag in tags:
			if tag.recipe_id not in tag_id_list:
				tag_id_list.append(tag.recipe_id)

		# recipe_id=tag_id_list yapabilir miyim? (liste verebilir miyim?)
		return Recipe.query.filter_by(recipe_id=tag_id_list).all()


	@staticmethod
	def find_by_details(details):
		return Recipe.query.filter_by(details=details).all()


	@staticmethod
	def find_by_contents(contents):
		return Recipe.query.filter_by(contents=contents).all()


	def get_liked_posts(user_id):
		ids = Like.get_liked_by_user_id(user_id)
		



	@staticmethod
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
		_recipe.score = self.score
		_recipe.user_id = self.user_id
		db.session.commit()


	def delete_recipe(self):
		deleted_recipe_id = self.id
		Recipe.query.filter_by(id=self.id).delete()
		db.session.commit()
		return self.id


	def increase_view(self):
		self.views = self.views + 1
		db.session.commit()


db.create_all()

	
