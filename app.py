from flask import Flask
from flask_restful import Resource, reqparse, Api

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

from base import Recipe, db
db.init_app(app)
app.app_context().push()
db.create_all()

class All_Recipes(Resource):
    def get(self):
        return {'Recipes': list(map(lambda x: x.json(), Recipe.query.all()))}

api.add_resource(All_Recipes, '/')

if __name__=='__main__':

    app.run(debug=True)
