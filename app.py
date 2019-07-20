from run import app, db
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource, reqparse, Api
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, JWTManager
import json, os
from flask import make_response, send_file
from datetime import datetime
import atexit
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from pprint import pprint


api = Api(app)
jwt = JWTManager(app)

# from models import Recipe, User, Final_Photos, Ingredient_Photos, Step_Photos, Tags
from models import *
from routes import *

firebase_auth_key = "AAAAZEY1WHc:APA91bHMYfwQHlq5c0MCznhKo9hzBHkbil8kC0NCysEkgBR5kg3um5Q57_bZioed46ohS0XfL9wWP99lZ6a0EdmktN9cQ7RYmPxxCYBeF-bMJgC3YLc3d7EWAjzX5v5K3VOWPnhxTFdp"

# Delete recipe after a time.
def delete_recipe_automatically():
	with app.app_context():
		users = User.get_all_users()
		for user in users:
			recipes = Recipe.find_by_username(user.username)
			for recipe in recipes:
				if recipe.post_time == None:
					Recipe.delete_by_id(recipe.id)
				else:
					recipe_date = datetime.strptime(recipe.post_time, "%m/%d/%Y, %H:%M:%S")
					now = datetime.now()
					timedelta = int((now-recipe_date).total_seconds())
					if timedelta > user.recipe_delete_time: # delete recipes posted 10 hrs ago or more.
						Recipe.delete_by_id(recipe.id)
						print(recipe.post_time)
	'''
	with app.app_context():
		recipes = Recipe.get_all_recipes()
		for recipe in recipes:
			if recipe.post_time == None:
				Recipe.delete_by_id(recipe.id)
			else:
				recipe_date = datetime.strptime(recipe.post_time, "%m/%d/%Y, %H:%M:%S")
				now = datetime.now()
				timedelta = int((now-recipe_date).total_seconds())
				if timedelta > 60 * 60 * 10: # delete recipes posted 10 hrs ago or more.
					Recipe.delete_by_id(recipe.id)
					print(recipe.post_time)
	'''


scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_recipe_automatically, trigger="interval", seconds=15)
scheduler.start()

# Shutdown register when exiting the app.
atexit.register(lambda: scheduler.shutdown())

#mainlink = "http://localhost:5000"
mainlink = "https://foodrecipesbil495.herokuapp.com"


class All_Recipes(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('search_type', type=str, required=False, help='Type to be searched')
	parser.add_argument('searched_keyword', type=str, required=False, help='Searched keyword')

	def get(self):
		args = All_Recipes.parser.parse_args()
		print("Args-search_type: {}".format(args['search_type']))
		if args['search_type'] != None:
			# [('USERNAME', 'username'), ('NAME', 'recipe name'), ('TAG','tag'), ('CONTENT', 'content'), ('DETAILS', 'details')]
			if args['search_type'] == 'USERNAME':
				recipes = Recipe.find_by_username(args['searched_keyword'])
			elif args['search_type'] == 'NAME':
				recipes = Recipe.find_by_name(args['searched_keyword'])
			elif args['search_type'] == 'TAG':
				recipes = Recipe.find_by_tag_name(args['searched_keyword'])
			elif args['search_type'] == 'CONTENT':
				recipes = Recipe.find_by_contents(args['searched_keyword'])
			elif args['search_type'] == 'DETAILS':
				recipes = Recipe.find_by_details(args['searched_keyword'])
			else:
				recipes = db.session.query(Recipe).all()
		else:
			recipes = db.session.query(Recipe).all()

		_json = []
		for recipe in recipes:
			user = User.find_by_id(recipe.user_id)
			item = {}
			item['id'] = recipe.id
			item['name'] = recipe.name
			item['post_time'] = str(recipe.post_time)
			item['contents'] = recipe.contents
			item['username'] = user.username
			item['tags'] = Tags.find_by_recipe_id(recipe.id)
			item['details'] = recipe.details
			item['views'] = recipe.views
			item['likes'] = recipe.likes
			item['user_id'] = recipe.user_id
			_json.append(item)
		return _json
		# return {'Recipes': list(map(lambda x: x.json(), db.session.query(Recipe).all() ))}



class PostRecipe(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name', type=str, required=True, help='Name of the recipe')
	parser.add_argument('post_time', type=str, required=True, help='Date of the recipe needs to be checked')
	parser.add_argument('contents', type=str, required=True, help='Content of the recipe')
	parser.add_argument('details', type=str, required=True, help='Details of the recipe')
	parser.add_argument('tags', type=str, required=False, help='Tags of the recipe')

	@jwt_required
	def post(self):
		username = get_jwt_identity()
		user = User.find_by_username(username)
		id = user.id
		if id is None:
			return 400

		args = PostRecipe.parser.parse_args()
		print("Tags: ", args['tags'])
		item = Recipe(name=args['name'], contents=args['contents'], details=args['details'], views=0, user_id=id)
		item.post_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		recipe_id = item.add_recipe()


		if args['tags'] != "":
			for tag_name in args['tags'].split("-"):
				tag = Tags(recipe_id=recipe_id, name=tag_name)
				tag.add_tag()

		return jsonify(item=item.json(), status_code=200)


class GetRecipe(Resource):
	def get(self, recipeId):
		item = Recipe.find_by_id(recipeId)
		if item:
			Recipe.increase_view(item)
			user = User.find_by_id(item.user_id)
			_json = {}
			_json['id'] = item.id
			_json['name'] = item.name
			_json['contents'] = item.contents
			_json['details'] = item.details
			_json['username'] = user.username
			_json['tags'] = Tags.find_by_recipe_id(item.id)
			_json['post_time'] = str(item.post_time)
			_json['views'] = item.views
			_json['likes'] = item.likes
			_json['user_id'] = item.user_id
			pprint(_json)
			return _json, 200
		else:
			return {'Message': 'Recipe is not found.'}, 400
		# return jsonify(message='Recipe is not found', status_code=400)


class CheckAuthority(Resource):
	@jwt_required
	def get(self, recipeId):
		item = Recipe.find_by_id(recipeId)
		username = get_jwt_identity()
		user = User.find_by_username(username)
		if item.user_id != user.id:
			return {'Message': 'User {} is not authorized to do that'.format(username)}, 401
		else:
			return {'Message': 'User {} is authorized to do that.'.format(recipeId)}, 200


class CheckUserUpdateAuthority(Resource):
	@jwt_required
	def get(self, userId):
		username = get_jwt_identity()
		user = User.find_by_username(username)
		if userId != user.id:
			return {'Message': 'User {} is not authorized to do that'.format(username)}, 401
		else:
			return {'Message': 'User {} is authorized to do that.'.format(username)}, 200


class RecipeManipulation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name', type=str, required=True, help='Name of the recipe')
	parser.add_argument('contents', type=str, required=True, help='Content of the recipe')
	parser.add_argument('details', type=str, required=True, help='Details of the recipe')
	parser.add_argument('tags', type=str, required=False, help='Tags of the recipe')

	@jwt_required
	def delete(self, recipeId):
		item = Recipe.find_by_id(recipeId)
		if item:
			username = get_jwt_identity()
			user = User.find_by_username(username)
			if item.user_id != user.id:
				return {'Message': 'User {} is not authorized to do that'.format(username)}, 401
			else:
				Recipe.delete_by_id(recipeId)
				return {'Message': '{} has been deleted from records'.format(recipeId)}, 200
		else:
			return {'Message': '{} is already not on the list.'.format(recipeId)}, 200


	@jwt_required
	def put(self, recipeId):
		username = get_jwt_identity()
		user = User.find_by_username(username)
		id = user.id
		item = Recipe.find_by_id(recipeId)
		if item:
			if item.user_id != id:
				return {'Message': 'User {} is not authorized to do that'.format(username)}, 401
			else:
				args = RecipeManipulation.parser.parse_args()
				item.name = args['name']
				item.contents = args['contents']
				item.details = args['details']
				item.post_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
				item.delete_tags()
				item.update_recipe()

				if args['tags'] != "":
					for tag_name in args['tags'].split("-"):
						tag = Tags(recipe_id=item.id, name=tag_name)
						tag.add_tag()
				return {'Message': '{} has been updated.'.format(recipeId)}, 200
		else:
			return {'Message': '{} is already not on the list.'.format(recipeId)}, 200


class UserList(Resource):
	def get(self, userId):
		user = User.find_by_Id(userId)
		if user:
			# return user.json()
			# return jsonify(users=user.json, status_code=200)
			return {'users': user.json}, 200
		return {'Message': 'User not found.'}, 404


class UserManipulation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('password', type=str, required=True, help='Password of user')
	parser.add_argument('recipe_delete_time', type=str, required=True, help='Time to delete recipe')

	@jwt_required
	def get(self, userId):
		user = User.find_by_id(userId)
		_json = {}
		_json['password'] = user.password
		_json['recipe_delete_time'] = user.recipe_delete_time
		return _json, 200

	@jwt_required
	def put(self, userId):
		user = User.find_by_id(userId)
		if user:
			args = UserManipulation.parser.parse_args()
			print("RECIPE DELETE TIME: {}".format(args['recipe_delete_time']))
			_user = User(user.username, args['password'], args['recipe_delete_time'])
			User.update_user(_user, userId)
			return {'Message': 'User info updated.'}, 200
		else:
			return {'Message': 'User not found.'}, 404

	@jwt_required
	def delete(self,userId):
		try:
			User.delete_by_id(userId)
		except:
			return {'Message': 'User could not deleted.'}, 400
		return {'Message': 'User successfully deleted.'}, 200

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help='Name of the user')
	parser.add_argument('password', type=str, required=True, help='Password of the user')

	def post(self):
		args = UserRegister.parser.parse_args()
		if User.find_by_username(args["username"]):
			return {'Message': 'User exists!'}, 400


		user = User(args["username"], args["password"])
		user.add_user()
		return {'Message': 'User {} created!'.format(args['username'])}, 200


class UserActivation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('access_token', type=str, required=True, help='Access Token')


	def post(self):
		args = UserActivation.parser.parse_args()
		if args['access_token']:
			print("Access token found in UserActivation-post")
			return True
		else:
			print("Access token not found in UserActivation-post")
			return False


class GetUsername(Resource):
	@jwt_required
	def post(self):
		username = get_jwt_identity()
		return {'username': username}, 200


class GetUserId(Resource):
	@jwt_required
	def post(self):
		username = get_jwt_identity()
		user = User.find_by_username(username)
		return {'user_id': user.id}, 200


class UserLogin(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help='Name of the user')
	parser.add_argument('password', type=str, required=True, help='Password of the user')

	def post(self):
		args = UserLogin.parser.parse_args()
		user =  User.find_by_username(args["username"])

		if user and user.password == args["password"]:
			access_token = create_access_token(identity=user.username, fresh=True)
			refresh_token = create_refresh_token(identity=user.username)
			return {'access_token': access_token, 'refresh_token': refresh_token}, 200

		return {'Message': 'Invalid credentials!'}, 401


class UserRecipes(Resource):
	def get(self, username):
		user = User.find_by_username(username)
		print("User-username: {}-{}".format(user, username))
		if user:
			_json = []
			for recipe in User.get_recipe_list(user):
				user = User.find_by_id(recipe.user_id)
				item = {}
				item['id'] = recipe.id
				item['name'] = recipe.name
				item['username'] = user.username
				item['tags'] = Tags.find_by_recipe_id(recipe.id)
				item['post_time'] = str(recipe.post_time)
				item['contents'] = recipe.contents
				item['details'] = recipe.details
				item['views'] = recipe.views
				item['likes'] = recipe.likes
				item['user_id'] = recipe.user_id
				_json.append(item)
			print(_json)
			return _json

class FinalPhotoFormation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('tag', type=str, required=True, help='Tag of the photo')

	def post(self, recipe_id):
		args = FinalPhotoFormation.parser.parse_args()
		photo_tag = args['tag']
		file = request.files['final_photo']
		file.save(os.path.join('static/recipe_photos/', '{}.jpeg'.format(photo_tag)))
		newPhoto = Final_Photos(recipe_id, os.path.join('static/recipe_photos/', '{}.jpeg'.format(photo_tag)))
		newPhoto.create_to()

class QueryFinalPhotos(Resource):
	def get(self, recipe_id):
		_json= []
		for photo in Final_Photos.get_photos(recipe_id):
			item = {}
			item['photo_link'] = '{}/{}'.format(mainlink,photo.photo_link)
			_json.append(item)
		return _json

class IngredientPhotoFormation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('tag', type=str, required=True, help='Tag of the photo')

	def post(self, recipe_id):
		args = IngredientPhotoFormation.parser.parse_args()
		photo_tag = args['tag']
		file = request.files['ingredient_photo']
		file.save(os.path.join('static/recipe_photos/', '{}.jpeg'.format(photo_tag)))
		newPhoto = Ingredient_Photos(recipe_id, os.path.join('static/recipe_photos/', '{}.jpeg'.format(photo_tag)))
		newPhoto.create_to()

class QueryIngredientPhotos(Resource):
	def get(self, recipe_id):
		_json= []
		for photo in Ingredient_Photos.get_photos(recipe_id):
			item = {}
			item['photo_link'] = '{}/{}'.format(mainlink,photo.photo_link)
			_json.append(item)
		return _json

class StepPhotoFormation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('tag', type=str, required=True, help='Tag of the photo')

	def post(self, recipe_id):
		args = StepPhotoFormation.parser.parse_args()
		photo_tag = args['tag']
		file = request.files['step_photo']
		file.save(os.path.join('static/recipe_photos/', '{}.jpeg'.format(photo_tag)))
		newPhoto = Step_Photos(recipe_id, os.path.join('static/recipe_photos/', '{}.jpeg'.format(photo_tag)))
		newPhoto.create_to()

class QueryStepPhotos(Resource):
	def get(self, recipe_id):
		_json= []
		for photo in Step_Photos.get_photos(recipe_id):
			item = {}
			item['photo_link'] = '{}/{}'.format(mainlink,photo.photo_link)
			_json.append(item)
		return _json

class IncreaseLike(Resource):
	def post(self, recipe_id):
		recipe = Recipe.find_by_id(recipe_id)
		Recipe.increase_like(recipe)
		user = User.find_by_id(recipe.user_id)

		_json = {
 		"to" : user.device_id,
 		"collapse_key" : "type_a",
 		"notification" : {
     	"body" : "Bir kullanici senin tarifini begendi!",
     	"title": "Title of Your Notification"
 		},
 		"data" : {
     	"body" : "Body of Your Notification in Data",
     	"title": "Title of Your Notification in Title",
     	"key_1" : "Value for key_1",
     	"key_2" : "Value for key_2"
 	}
}
		headers = {
    	'Authorization': 'key=' + firebase_auth_key,
    	'Content-Type': 'application/json',
  			}

		resp = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(_json), headers=headers)

		return {'Message': 'User {} liked that.'.format(recipeId)}, 200

class PushLikeNotification(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('device_id', type=str, required=True, help='Device id')
	def post(self, username):
		args = PushLikeNotification.parser.parse_args()
		user = User.find_by_username(username)
		user.device_id = args['device_id']
		User.update_user(user, user.id)

@jwt.invalid_token_loader
def invalid_token_callback(self):
	return {'description': "Signature verification failed!", "error": "invalid_token"}, 401
	# return jsonify(description="Signature verification failed!", error="invalid_token", status_code=401)


@jwt.expired_token_loader
def expired_token_callback(self):
	return {'description': "Token has expired!!!", "error": "token_expired"}, 401
	# return jsonify(description="Token has expired!!!", error="token_expired", status_code=401)


@jwt.unauthorized_loader
def unauthorized_loader_callback(self):
	return {'description': "Access token not found!", "error": "unauthorized_loader"}, 401
	# return jsonify(description="Access token not found!", error="unauthorized_loader", status_code=401)


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback(self):
	return {'description': "Token is not fresh. Fresh token needed!", "error": "needs_fresh_token"}, 401
	# return jsonify(description="Token is not fresh. Fresh token needed!", error="needs_fresh_token", status_code=401)


api.add_resource(UserLogin, "/api/login")
api.add_resource(GetUsername, "/api/getUsername")
api.add_resource(GetUserId, "/api/getUserId")
api.add_resource(UserRegister, "/api/register")
api.add_resource(UserList, "/api/getUserInfo/<int:userId>")
api.add_resource(UserManipulation, "/api/userManipulation/<int:userId>")
api.add_resource(UserRecipes, '/api/getUserRecipes/<string:username>')
api.add_resource(RecipeManipulation, '/api/recipeManipulation/<int:recipeId>')
api.add_resource(GetRecipe, '/api/getRecipe/<int:recipeId>')
api.add_resource(PostRecipe, '/api/addRecipe')
api.add_resource(FinalPhotoFormation, '/api/<int:recipe_id>/finalphoto')
api.add_resource(QueryFinalPhotos, '/api/<int:recipe_id>/finalphoto')
api.add_resource(IngredientPhotoFormation, '/api/<int:recipe_id>/ingredientphoto')
api.add_resource(QueryIngredientPhotos, '/api/<int:recipe_id>/ingredientphoto')
api.add_resource(StepPhotoFormation, '/api/<int:recipe_id>/stepphoto')
api.add_resource(QueryStepPhotos, '/api/<int:recipe_id>/stepphoto')
api.add_resource(All_Recipes, '/api/showAllRecipes')
api.add_resource(CheckAuthority, '/api/checkAuthority/<int:recipeId>')
api.add_resource(CheckUserUpdateAuthority, '/api/checkUserUpdateAuthority/<int:userId>')
api.add_resource(UserActivation, "/amiactive")
api.add_resource(IncreaseLike, '/api/<int:recipe_id>/like')
api.add_resource(PushLikeNotification, '/api/<string:username>/deviceid')
