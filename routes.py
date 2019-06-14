from run import app, db
from flask import render_template, url_for, flash, redirect, request, session
from models import Recipe, User
from forms import AddRecipeForm, UserRegistrationForm, UserLoginForm
import requests
from flask import jsonify
from pprint import pprint
import os


# mainlink = "http://localhost:5000"
mainlink = "https://foodrecipesbil495.herokuapp.com"

def chk_session():
	try:
		if session['access_token']:
			flash("Access token found", 'success')
			return True
		else:
			print("Access token is None", 'success')
			return False
	except:
		print("Access token is not initialized", 'success')
		return False


@app.route("/addrecipe", methods=['GET', 'POST'])
def addrecipe():
	if chk_session():
		form = AddRecipeForm()
		if form.validate_on_submit():
			_json = {
				'name': form.name.data,
				'post_time' : "2011-10-05T23:31:12",
				'contents': form.contents.data,
				'details': form.details.data
			}
			response = requests.post(url="{}/recipe".format(mainlink), params=_json, headers={"Authorization": "Bearer {}".format(session['access_token'])})
			flash('Recipe Added.', 'success')
			return redirect(url_for('allrecipes'))
		else:
			return render_template('addrecipe.html', form=form, title="Add Recipe")
	else:
		return redirect(url_for('login'))
	

@app.route("/allrecipes")
def allrecipes():
	recipes = requests.get(url="{}/showrecipes".format(mainlink)).json()['Recipes']
	return render_template('allrecipes.html', recipes=recipes, title="All Recipes")


@app.route("/myrecipes")
def myrecipes():
	if chk_session():
		response = requests.post(url="{}/getusername".format(mainlink), headers={"Authorization": "Bearer {}".format(session['access_token'])})
		if response.status_code == 200:
			username = response.json()['username']
			recipes = requests.get(url="{}/user/{}".format(mainlink, username), headers={"Authorization": "Bearer {}".format(session['access_token'])}).json()
			pprint(recipes)
			return render_template('myrecipes.html', recipes=recipes, title="My Recipes")
		else:
			flash('No user found.', 'error')
			return redirect(url_for('login'))
	else:
		flash('Please login first.', 'error')
		return redirect(url_for('login'))




@app.route("/signup", methods=['GET', 'POST'])
def signup():

	if chk_session():
		return redirect(url_for('myrecipes'))
	else:
		form = UserRegistrationForm()
		flash("Hata: {}".format(form.errors))
		if form.validate_on_submit():
			_json = {
				'username': form.username.data,
				'password': form.password.data
			}
			response = requests.post(url='{}/user'.format(mainlink), params=_json)
			if response.status_code != 200:
				flash('Username already exists.')
				return render_template('signup.html', title='Sign up', form=form)
			flash('{} adli hesap olusturuldu.'.format(form.username.data), 'success')
			return redirect(url_for('login'))
		else:
			flash("Buraya girdi.", 'success')
			return render_template('signup.html', title='Sign up', form=form)


# Don't change it's name. to trigger @login_required decorator, it needs to be named as login.
@app.route("/", methods=['GET', 'POST'])
def login():
	if chk_session():
		return redirect(url_for('myrecipes'))
	else:
		form = UserLoginForm()
		flash("Hata: {}".format(form.errors))
		if form.validate_on_submit():
			_json = {
				'username': form.username.data,
				'password': form.password.data
			}
			response = requests.post(url='{}/loginnn'.format(mainlink), params=_json)
			if response.status_code == 200:
				access_token = response.json()['access_token']
				session['access_token'] = access_token
				return redirect(url_for('myrecipes'))

			else:
				flash("No user found", 'success')
				return render_template('signin.html', title='Sign in', form=form)
		else:
			# first enter goes here.
			return render_template('signin.html', title='Sign in', form=form)



@app.route("/signout")
def signout():
	session.pop('access_token', None)
	return redirect(url_for('login'))


@app.route("/deleterecipe/<string:recipe_name>", methods=['POST', 'GET'])
def deleterecipe(recipe_name):
	if chk_session():
		response = requests.delete(url="{}/recipe/{}".format(mainlink, recipe_name), headers={"Authorization": "Bearer {}".format(session['access_token'])})
		if response.status_code == 200:
			flash('Item successfully deleted.', 'success')
		else:
			flash('Item did not deleted', 'error')
		return redirect(url_for('allrecipes'))
	else:
		flash('Please login first.', 'error')
		return redirect(url_for('login'))
	

# Update isini Ahmet Utku ile konus.
# Change addrecipe, so you can update recipe too.
# Check it has recipe_name param.
@app.route("/updaterecipe/<string:recipe_name>", methods=['POST', 'GET'])
def updaterecipe(recipe_name):
	if chk_session():
		response = requests.update(url="{}/recipe/{}".format(mainlink, recipe_name), headers={"Authorization": "Bearer {}".format(session['access_token'])})
		if response.status_code == 200:
			flash('Item successfully updated.', 'success')
		else:
			flash('Item did not updated', 'error')
		return redirect(url_for('allrecipes'))
	
	else:
		flash('Please login first.', 'error')
		return redirect(url_for('login'))
	