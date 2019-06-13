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

    @jwt_required
    def post(self):
        username = get_jwt_identity()
        print("username" + username)
        user = User.find_by_username(User, username)
        id = user.id
        if id is None:
            return 400
        args = RecipeFormation.parser.parse_args()
        if Recipe.find_by_name(Recipe, args['name']):
            return {' Message': 'Recipe with the name {} already exists'.format(args['name'])}
        item = Recipe(name=args['name'], post_time=args['post_time'], contents=args['contents'], details=args['details'], views=0, score=0, user_id=id)
        item.create_to()
        return item.json()


class RecipeManipulation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Name of the recipe')
    parser.add_argument('contents', type=str, required=True, help='Content of the recipe')

    def get(self, recipeName):
        item = Recipe.find_by_name(Recipe, recipeName)
        if item:
            Recipe.increase_view(item)
            return item.json()
        return {'Message': 'Recipe is not found'}

    @jwt_required
    def delete(self, recipeName):
        username = get_jwt_identity()
        user = User.find_by_username(User, username)
        id = user.id
        item = Recipe.find_by_name(Recipe, recipeName)
        if item:
            if item.user_id != id:
                return {'Message': 'User {} is not authorized to do that'.format(username)}, 401
            Recipe.delete_by_Name(Recipe, recipeName)
            return {'Message': '{} has been deleted from records'.format(recipeName)}
        return {'Message': '{} is already not on the list'.format(recipeName)}


class UserList(Resource):
    def get(self, userId):
        user = User.find_by_Id(userId)
        if user:
            return user.json()
        return {
                   "message": "User not found!"
               }, 404


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Name of the user')
    parser.add_argument('password', type=str, required=True, help='Password of the user')

    def post(self):
        args = UserRegister.parser.parse_args()
        if User.find_by_username(User, args["username"]):
            return {
                       "message": "User exists!"
                   }, 400

        user = User(args["username"], args["password"])
        user.create_to()
        return {
            "message": "User {} created!".format(args["username"])
        }


class UserActivation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('access_token', type=str, required=True, help='Access Token')

    
    def post(self):
        args = UserActivation.parser.parse_args()
        if args['access_token']:
            print("Nice Access Token.")
            return True
        else:
            print("There is no Access Token!!!")
            return False


class GetUsername(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        print("*************Username: {}".format(username))
        return {
                   "username": username
               }, 200



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

            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {
                   "message": "Invalid credentials!"
               }, 401


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


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
        }, 401
    )


@jwt.invalid_token_loader
def invalid_token_callback(self):
    return jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
        }, 401
    )


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify(
        {
            "description": "Access token not found!",
            "error": "unauthorized_loader"
        }, 401
    )


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback():
    return jsonify(
        {
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }, 401
    )


# api.add_resource(All_Recipes, '/debugrecipes')

api.add_resource(RecipeFormation, '/recipe')
api.add_resource(RecipeManipulation, '/recipe/<string:recipeName>')
api.add_resource(UserRecipes, '/recipe/<string:username>')
api.add_resource(UserList, "/user/<int:userId>")
api.add_resource(UserRegister, "/user")
api.add_resource(UserLogin, "/login")
api.add_resource(UserActivation, "/amiactive")
api.add_resource(GetUsername, "/getusername")


