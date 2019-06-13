from run import app, db
from flask import render_template, url_for, flash, redirect, request
from models import Recipe, User
from forms import AddRecipeForm, UserRegistrationForm, UserLoginForm
import requests
from flask import jsonify
from pprint import pprint


access_token = None
			 
@app.route("/addrecipe", methods=['GET', 'POST'])
def addrecipe():
	form = AddRecipeForm()
	if form.validate_on_submit():
		_json = {
			'name': form.name.data,
			'post_time' : "2011-10-05T23:31:12",
			'contents': form.contents.data,
			'details': form.details.data
		}

		response = requests.post(url="http://localhost:5000/recipe", params=_json, headers={"Authorization": "Bearer {}".format(access_token)})
		flash('Recipe Added.', 'success')
		return redirect(url_for('allrecipes'))
	else:	
		return render_template('addrecipe.html', form=form, title="Add Recipe", access_token=access_token)


@app.route("/allrecipes")
def allrecipes():
	recipes = Recipe.query.all()
	return render_template('allrecipes.html', recipes=recipes, title="All Recipes", access_token=access_token)


@app.route("/myrecipes")
def myrecipes():
	if requests.post(url="http://localhost:5000/amiactive", params={"access_token": access_token}):
		response = requests.post(url="http://localhost:5000/getusername", headers={"Authorization": "Bearer {}".format(access_token)})
		if response.status_code == 200:
			username = response.json()['username']
			recipes = requests.get(url="http://localhost:5000/recipe/{}".format(username), headers={"Authorization": "Bearer {}".format(access_token)}).json()
			return render_template('myrecipes.html', recipes=recipes, title="My Recipes", access_token=access_token)
		else:
			flash('No user found.', 'error')
			return redirect(url_for('login'))
	else:
		flash('Please login first.', 'error')
		return redirect(url_for('login'))
	
	


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if requests.post(url="http://localhost:5000/amiactive", params={"access_token": access_token}):
		return redirect(url_for('myrecipes'))
	else:
		form = UserRegistrationForm()
		if form.validate_on_submit():

			flash('{} adli hesap olusturuldu.'.format(form.username.data), 'success')
			return redirect(url_for('login'))
		else:
			return render_template('signup.html', title='Sign up', form=form, access_token=access_token)


# Don't change it's name. to trigger @login_required decorator, it needs to be named as login. 
@app.route("/", methods=['GET', 'POST'])
def login():
	global access_token

	form = UserLoginForm()
	if form.validate_on_submit():
		_json = {
			'username': form.username.data,
			'password': form.password.data
		}
		response = requests.post(url='http://localhost:5000/loginnn', params=_json)
		if response.status_code == 200:
			access_token = response.json()['access_token']
			return redirect(url_for('myrecipes'))

		else:
			flash("No user found", 'success')
			return redirect(url_for('login'))

	else:
		return render_template('signin.html', title='Sign in', form=form)


@app.route("/signout")
def signout():
	global access_token
	access_token = None
	return redirect(url_for('login'))


@app.route("/deleterecipe/<string:recipe_name>", methods=['POST', 'GET'])
def deleterecipe(recipe_name):
	print("data: ")
	return redirect(url_for('allrecipes'))


# Change addrecipe, so you can update recipe too.
# Check it has recipe_name param.
@app.route("/updaterecipe/<string:recipe_name>", methods=['POST', 'GET'])
def updaterecipe(recipe_name):
	print("data: ")
	return redirect(url_for('addrecipe', recipe_name=recipe_name))
