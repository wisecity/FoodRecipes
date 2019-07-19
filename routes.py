from run import app, db
from flask import render_template, url_for, flash, redirect, request, session
from models import Recipe, User
from forms import AddRecipeForm, UserRegistrationForm, UserLoginForm, SearchForm
import requests
from flask import jsonify
from pprint import pprint
from datetime import datetime
import os
from werkzeug.datastructures import MultiDict


#mainlink = "http://localhost:5000"
mainlink = "https://foodrecipesbil495.herokuapp.com"

# session login olunmadiginda init edilmemis oluyor.
# session login olunca 'access_token' elemani ekleniyor.
# logout yapilinca session objesi hala var, session['access_token'] = None
def chk_session():
	try:
		if session['access_token']:
			# flash("Access token found", 'success')
			return True
		else:
			# print("Access token is None", 'success')
			return False
	except:
		# print("Access token is not initialized", 'success')
		return False


@app.route("/register", methods=['GET', 'POST'])
def register():

	if chk_session():
		return redirect(url_for('myrecipes'))
	else:
		form = UserRegistrationForm()
		if form.is_submitted():
			_json = {
				'username': form.username.data,
				'password': form.password.data
			}
			response = requests.post(url='{}/api/register'.format(mainlink), params=_json)
			print(response)
			print(response.status_code)
			print("===================")
			if response.status_code != 200:
				flash('Username already exists.')
				return render_template('register.html', title='Register', form=form)
			flash('{} adli hesap olusturuldu.'.format(form.username.data), 'success')
			return redirect(url_for('login'))
		else:
			flash("Buraya girdi.", 'warning')
			return render_template('register.html', title='Register', form=form)


# Don't change it's name. to trigger @login_required decorator, it needs to be named as login.
@app.route("/", methods=['GET', 'POST'])
def login():
	if chk_session():
		return redirect(url_for('myrecipes'))
	else:
		form = UserLoginForm()
		if form.is_submitted():
			_json = {
				'username': form.username.data,
				'password': form.password.data
			}
			response = requests.post(url='{}/api/login'.format(mainlink), params=_json)
			print(response)
			print(response.status_code)
			print("===================")
			if response.status_code == 200:
				access_token = response.json()['access_token']
				session['access_token'] = access_token
				return redirect(url_for('myrecipes'))

			else:
				flash("No user found", 'success')
				return render_template('login.html', title='Sign in', form=form)
		else:
			# first enter goes here.
			return render_template('login.html', title='Sign in', form=form)


@app.route("/logout")
def logout():
	session.pop('access_token', None)
	return redirect(url_for('login'))


@app.route("/allrecipes", methods=['GET', 'POST'])
def allrecipes():
	form = SearchForm()
	if form.is_submitted():
		_json = {'search_type': form.search_type.data, 'searched_keyword': form.searched_keyword.data}
		recipes = requests.get(url="{}/api/showAllRecipes".format(mainlink), params=_json).json()
	else:
		recipes = requests.get(url="{}/api/showAllRecipes".format(mainlink)).json()
	# pprint(recipes)
	return render_template('allrecipes.html', recipes=recipes, title="All Recipes", form=form)


@app.route("/myrecipes")
def myrecipes():
	if chk_session():
		response = requests.post(url="{}/api/getUsername".format(mainlink), headers={"Authorization": "Bearer {}".format(session['access_token'])})
		print(response)
		print(response.status_code)
		if response.status_code == 200:
			username = response.json()['username']
			recipes = requests.get(url="{}/api/getUserRecipes/{}".format(mainlink, username), headers={"Authorization": "Bearer {}".format(session['access_token'])}).json()
			pprint(recipes)
			return render_template('myrecipes.html', recipes=recipes, title="My Recipes")
		else:
			flash('No user found.', 'danger')
			return redirect(url_for('login'))
	else:
		flash('Please login first.', 'danger')
		return redirect(url_for('login'))


@app.route("/addrecipe", methods=['GET', 'POST'])
def addrecipe():
	if chk_session():
		now = datetime.now()
		form = AddRecipeForm()
		if form.is_submitted():
			_json = {
				'name': form.name.data,
				'post_time' : now.strftime("%m/%d/%Y, %H:%M:%S"),
				'contents': form.contents.data,
				'details': form.details.data,
				'tags': form.tags.data
			}
			response = requests.post(url="{}/api/addRecipe".format(mainlink), params=_json, headers={"Authorization": "Bearer {}".format(session['access_token'])})
			if response.status_code == 200:
				flash('Recipe already exists', 'success')
			else:
				flash('Recipe Added.', 'success')
			return redirect(url_for('allrecipes'))
		else:
			return render_template('addrecipe.html', form=form, title="Add Recipe")
	else:
		flash('Please login first.', 'danger')
		return redirect(url_for('login'))


@app.route("/deleterecipe/<int:recipe_id>", methods=['POST', 'GET'])
def deleterecipe(recipe_id):
	if chk_session():
		response = requests.delete(url="{}/api/recipeManipulation/{}".format(mainlink, recipe_id), headers={"Authorization": "Bearer {}".format(session['access_token'])})
		print(response)
		print(response.status_code)
		if response.status_code == 200:
			flash('Item successfully deleted.', 'success')
		else:
			flash('You are not authorized to delete this item.', 'danger')
		return redirect(url_for('allrecipes'))
	else:
		flash('Please login first.', 'danger')
		return redirect(url_for('login'))


# Update isini Ahmet Utku ile konus.
# Change addrecipe, so you can update recipe too.
# Check it has recipe_name param.
@app.route("/updaterecipe/<int:recipe_id>", methods=['POST', 'GET'])
def updaterecipe(recipe_id):
	if chk_session():
		now = datetime.now()
		authority_response = requests.get(url="{}/api/checkAuthority/{}".format(mainlink, recipe_id), headers={"Authorization": "Bearer {}".format(session['access_token'])})
		print(authority_response)
		if authority_response.status_code == 200:
			response = requests.get(url="{}/api/getRecipe/{}".format(mainlink, recipe_id), headers={"Authorization": "Bearer {}".format(session['access_token'])}).json()
			autofill_dict = MultiDict({'name': response['name'], 'contents': response['contents'], 'details': response['details'], 'tags': response['tags']})
			if request.method == 'GET':
				form = AddRecipeForm(formdata=autofill_dict)
			else:
				form = AddRecipeForm()
			if form.is_submitted():
				_json = {
					'name': form.name.data,
					'post_time' : now.strftime("%m/%d/%Y, %H:%M:%S"),
					'contents': form.contents.data,
					'details': form.details.data,
					'tags': form.tags.data
				}
				print(form.name.data, "+++++")
				response = requests.put(url="{}/api/recipeManipulation/{}".format(mainlink, recipe_id), params=_json, headers={"Authorization": "Bearer {}".format(session['access_token'])})
				print(response.json())
				print(response.status_code)
				flash('Recipe Updated.', 'success')
				return redirect(url_for('recipedetails', recipe_id=recipe_id))
			else:
				return render_template('updaterecipe.html', form=form, title="Update Recipe")
		else:
			flash('You are not authorized to update this.', 'danger')
			return redirect(url_for('myrecipes'))
	else:
		flash('Please login first.', 'danger')
		return redirect(url_for('login'))


@app.route("/recipedetails/<int:recipe_id>", methods=['POST', 'GET'])
def recipedetails(recipe_id):
	if chk_session():
		response = requests.get(url="{}/api/getRecipe/{}".format(mainlink, recipe_id), headers={"Authorization": "Bearer {}".format(session['access_token'])})
		recipe = response.json()
		response = requests.get(url="{}/api/{}/finalphoto".format(mainlink, recipe_id))
		final_photos = response.json()
		response = requests.get(url="{}/api/{}/ingredientphoto".format(mainlink, recipe_id))
		ingredient_photos = response.json()
		response = requests.get(url="{}/api/{}/stepphoto".format(mainlink, recipe_id))
		step_photos = response.json()
		return render_template('recipedetails.html', recipe=recipe, final_photos = final_photos, ingredient_photos = ingredient_photos, step_photos = step_photos)
	else:
		flash('Please login first.', 'danger')
		return redirect(url_for('login'))


@app.route('/addfinalphoto', methods=['POST'])
def uploadFinalPhoto():
    tag = {'tag' : request.form['photo_tag']}
    file = request.files['file']
    file.save(os.path.join('static', 'temp.jpeg'))
    respond = requests.post("{}/api/{}/finalphoto".format(mainlink, request.form['recipe_id']), params = tag, files={'final_photo' : open('static/temp.jpeg', 'rb')})
    return redirect(url_for('recipedetails', recipe_id = request.form['recipe_id']))


@app.route('/addingredientphoto', methods=['POST'])
def uploadIngredientPhoto():
    tag = {'tag' : request.form['photo_tag']}
    file = request.files['file']
    file.save(os.path.join('static', 'temp.jpeg'))
    respond = requests.post("{}/api/{}/ingredientphoto".format(mainlink, request.form['recipe_id']), params = tag, files={'ingredient_photo' : open('static/temp.jpeg', 'rb')})
    return redirect(url_for('recipedetails', recipe_id = request.form['recipe_id']))


@app.route('/addstepphoto', methods=['POST'])
def uploadStepPhoto():
    tag = {'tag' : request.form['photo_tag']}
    file = request.files['file']
    file.save(os.path.join('static', 'temp.jpeg'))
    respond = requests.post("{}/api/{}/stepphoto".format(mainlink, request.form['recipe_id']), params = tag, files={'step_photo' : open('static/temp.jpeg', 'rb')})
    return redirect(url_for('recipedetails', recipe_id = request.form['recipe_id']))


@app.route("/webstats")
def get():
	return render_template('git_stats_web/activity.html')


@app.route("/androidstats")
def getAndroid():
	return render_template('git_stats_android/activity.html')
