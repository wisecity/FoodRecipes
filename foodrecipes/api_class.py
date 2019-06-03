from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort
from requests import put, get, post
from foodrecipes import db, app, api, bcrypt


users = []
recipes = []



class UserApi(Resource):
	def abort_if_doesnt_exist(self, user_id):
		if user_id not in users:
			abort(404, message="User {} doesn't exist".format(user_id))


	def get(self, user_id=None, username=None):
		if user_id != None:
			return make_response(jsonify(user_id=user_id), 200)
		else:
			return make_response(jsonify(username=username), 200)


	def put(self, user_id):
		parser = reqparse.RequestParser()
		parser.add_argument('username')
		parser.add_argument('password')
		args = parser.parse_args()
		hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')
		response = jsonify(id=user_id, username=args['username'], password=hashed_password)
		users.append(response)
		return make_response(response, 201)


	def delete(self, user_id):
		self.abort_if_doesnt_exist(user_id)
		del users[user_id]
		return make_response('', 204)


class UsersApi(Resource):
	def get(self):
		global users
		response = jsonify(users)
		response.status_code = 200
		return make_response(response)

	def delete(self):
		global users
		users = {}
		return make_response('', 204)


class RecipeApi(Resource):
	def abort_if_doesnt_exist(self, recipe_id):
		if recipe_id not in recipes:
			abort(404, message="Recipe {} doesn't exist".format(recipe_id))


	def get(self, recipe_id):
		return make_response(jsonify(id=recipe_id, name=name, contents=contents, score=score), 200)


	def put(self, recipe_id):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('contents')
		parser.add_argument('score')
		args = parser.parse_args()
		response = jsonify(id=recipe_id, name=name, contents=contents, score=score)
		recipes.append(response)
		return make_response(response, 201)


	def delete(self, recipe_id):
		self.abort_if_doesnt_exist(recipe, user_id)
		del recipes[recipe_id]
		return make_response('', 204)


class RecipesApi(Resource):
	def get(self):
		global recipes
		response = jsonify(recipes)
		response.status_code = 200
		return make_response(response)

	def delete(self):
		global recipes
		recipes = {}
		return make_response('', 204)


api.add_resource(UserApi, '/users/<int:user_id>', '/users/<string:username>')
api.add_resource(UsersApi, '/users')
api.add_resource(RecipeApi, '/recipes/<int:recipe_id>')
api.add_resource(RecipesApi, '/recipes')
# api.add_resource(UserApi, '/user/<int:todo_id>', endpoint="todo-ep")