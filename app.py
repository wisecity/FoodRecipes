from datetime import datetime
from flask import Flask, jsonify
from flask_restful import Resource, reqparse, Api
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required, JWTManager


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "lSc-eEq-Qvd"
jwt = JWTManager(app)

from base import Recipe, User, db
from routes import *
db.init_app(app)
app.app_context().push()
db.create_all()

class All_Recipes(Resource):
    def get(self):
        return {'Recipes': list(map(lambda x: x.json(), Recipe.query.all()))}

class RecipeFormation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Name', type=str, required=True, help='Name of the recipe')
    parser.add_argument('PostTime', type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), required=True, help='Date of the recipe needs to be checked')
    parser.add_argument('Contents', type=str, required=True, help='Content of the recipe')
    parser.add_argument('Details', type=str, required=True, help='Details of the recipe')

    @fresh_jwt_required
    def post(self):
        username = get_jwt_identity()
        user = User.find_by_username(User, username)
        id = user.Id
        if id is None:
            return
        args = RecipeFormation.parser.parse_args()
        if Recipe.find_by_name(Recipe, args['Name']):
            return {' Message': 'Recipe with the name {} already exists'.format(args['Name'])}
        item = Recipe(args['Name'], args['PostTime'], args['Contents'], args['Details'], 0, 0, id)
        item.create_to()
        return item.json()

class RecipeManipulation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Name', type=str, required=True, help='Name of the recipe')
    parser.add_argument('Contents', type=str, required=True, help='Content of the recipe')

    def get(self, recipeName):
        item = Recipe.find_by_name(Recipe, recipeName)
        if item:
            Recipe.increase_view(item)
            return item.json()
        return {'Message': 'Recipe is not found'}

    @fresh_jwt_required
    def delete(self, recipeName):
        username = get_jwt_identity()
        user = User.find_by_username(User, username)
        id = user.Id
        item = Recipe.find_by_name(Recipe, recipeName)
        if item:
            if item.Uid != id:
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
    parser.add_argument('Username', type=str, required=True, help='Name of the user')
    parser.add_argument('Password', type=str, required=True, help='Password of the user')

    def post(self):
        args = UserRegister.parser.parse_args()
        if User.find_by_username(User, args["Username"]):
            return {
                       "message": "User exists!"
                   }, 400

        user = User(args["Username"], args["Password"])
        user.create_to()
        return {
            "message": "User {} created!".format(args["Username"])
        }

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Username', type=str, required=True, help='Name of the user')
    parser.add_argument('Password', type=str, required=True, help='Password of the user')

    def post(self):
        args = UserRegister.parser.parse_args()

        user =  User.find_by_username(User, args["Username"])

        if user and user.Password == args["Password"]:
            access_token = create_access_token(identity=user.Username, fresh=True)
            refresh_token = create_refresh_token(identity=user.Username)

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
            return User.get_recipe_list(user)

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


api.add_resource(All_Recipes, '/')
api.add_resource(RecipeFormation, '/recipe')
api.add_resource(RecipeManipulation, '/recipe/<string:recipeName>')
api.add_resource(UserRecipes, '/user/<string:username>')
api.add_resource(UserList, "/user/<int:userId>")
api.add_resource(UserRegister, "/user")
api.add_resource(UserLogin, "/login")

if __name__=='__main__':

    app.run(debug=True)
