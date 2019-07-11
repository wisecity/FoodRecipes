from run import app, db
from datetime import datetime
from flask import jsonify
from flask_restful import Resource, reqparse, Api
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, JWTManager
import json

api = Api(app)
jwt = JWTManager(app)

from models import Recipe, User
from routes import *


class All_Recipes(Resource):
	def get(self):
		return {'Recipes': list(map(lambda x: x.json(), Recipe.query.all()))}


class RecipeFormation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name', type=str, required=True, help='Name of the recipe')
	parser.add_argument('post_time', type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), required=True, help='Date of the recipe needs to be checked')
	parser.add_argument('contents', type=str, required=True, help='Content of the recipe')
	parser.add_argument('details', type=str, required=True, help='Details of the recipe')
	parser.add_argument('tags', type=str, required=False, help='Tags of the recipe')

	@jwt_required
	def post(self):
		username = get_jwt_identity()
		print("username: " + username)
		user = User.find_by_username(User, username)
		id = user.id
		if id is None:
			return jsonify(status_code=400)
		args = RecipeFormation.parser.parse_args()
		print(args['tags'])
		if Recipe.find_by_name(Recipe, args['name']):
			return jsonify(message='Recipe with the name {} already exists'.format(args['name']), status_code=200)
		item = Recipe(name=args['name'], post_time=args['post_time'], contents=args['contents'], details=args['details'], views=0, score=0, user_id=id)
		item.create_to()

		if args['tags'] != "":
			for tag in args['tags'].split("-"):
				tag = Tags(name=tag)
		return jsonify(item=item.json(), status_code=200)


class RecipeManipulation(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name', type=str, required=True, help='Name of the recipe')
	parser.add_argument('contents', type=str, required=True, help='Content of the recipe')

	def get(self, recipeName):
		item = Recipe.find_by_name(Recipe, recipeName)
		if item:
			Recipe.increase_view(item)
			return item.json()
		return jsonify(message='Recipe is not found', status_code=400)


	@jwt_required
	def delete(self, recipeName):
		username = get_jwt_identity()
		user = User.find_by_username(User, username)
		id = user.id
		item = Recipe.find_by_name(Recipe, recipeName)
		if item:
			if item.user_id != id:
				# return {'Message': 'User {} is not authorized to do that'.format(username)}, 401
				return jsonify(message='User is not authorized to do that'.format(username), status_code=401)
			else:
				Recipe.delete_by_name(Recipe, recipeName)
				return jsonify(message='{} has been deleted from records'.format(recipeName), status_code=200)
		else:
			return jsonify(message='{} is already not on the list'.format(recipeName), status_code=200)


	@jwt_required
	def put(self, recipeName):
		username = get_jwt_identity()
		user = User.find_by_username(User, username)
		id = user.id
		item = Recipe.find_by_name(Recipe, recipeName)
		if item:
			if item.user_id != id:
				# return {'Message': 'User {} is not authorized to do that'.format(username)}, 401
				return jsonify(message='User {} is not authorized to do that'.format(username), status_code=401)
			else:
				item.update_(Recipe)
				return jsonify(message='{} has been updated.'.format(recipeName), status_code=200)
		else:
			return jsonify(message='{} is already not on the list'.format(recipeName), status_code=200)


class UserList(Resource):
	def get(self, userId):
		user = User.find_by_Id(userId)
		if user:
			# return user.json()
			return jsonify(users=user.json, status_code=200)
		return jsonify(message='User not found.', status_code=404)


class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help='Name of the user')
	parser.add_argument('password', type=str, required=True, help='Password of the user')

	def post(self):
		args = UserRegister.parser.parse_args()
		if User.find_by_username(User, args["username"]):
			return jsonify(message='User exists!', status_code=400)


		user = User(args["username"], args["password"])
		user.create_to()
		return jsonify(message='User {} created!'.format(args['username']), status_code=200)


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
		return jsonify(username=username, status_code=200)



class UserLogin(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help='Name of the user')
	parser.add_argument('password', type=str, required=True, help='Password of the user')

	def post(self):
		args = UserRegister.parser.parse_args()
		user =  User.find_by_username(User, args["username"])

		if user and user.password == args["password"]:
			access_token = create_access_token(identity=user.username, fresh=True)
			refresh_token = create_refresh_token(identity=user.username)
			return jsonify(access_token=access_token, refresh_token=refresh_token, status_code=200)

		return jsonify(message='Invalid credentials!', status_code=401)


class UserRecipes(Resource):
	def get(self, username):
		user = User.find_by_username(User, username)
		if user:
			_json = []
			for recipe in User.get_recipe_list(user):

				item = {}
				item['id'] = recipe.id
				item['name'] = recipe.name
				item['post_time'] = str(recipe.post_time)
				item['contents'] = recipe.contents
				item['details'] = recipe.details
				item['views'] = recipe.views
				item['score'] = recipe.score
				item['user_id'] = recipe.user_id
				_json.append(item)
			return _json


@jwt.invalid_token_loader
def invalid_token_callback(self):
	return jsonify(description="Signature verification failed!", error="invalid_token", status_code=401)


@jwt.expired_token_loader
def expired_token_callback(self):
	return jsonify(description="Token has expired!!!", error="token_expired", status_code=401)


@jwt.unauthorized_loader
def unauthorized_loader_callback(self):
	return jsonify(description="Access token not found!", error="unauthorized_loader", status_code=401)


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback(self):
	return jsonify(description="Token is not fresh. Fresh token needed!", error="needs_fresh_token", status_code=401)


api.add_resource(All_Recipes, '/showrecipes')
api.add_resource(RecipeFormation, '/recipe')
api.add_resource(RecipeManipulation, '/recipe/<string:recipeName>')
api.add_resource(UserRecipes, '/user/<string:username>')
api.add_resource(UserList, "/user/<int:userId>")
api.add_resource(UserRegister, "/user")
api.add_resource(UserLogin, "/loginnn")
api.add_resource(UserActivation, "/amiactive")
api.add_resource(GetUsername, "/getusername")
