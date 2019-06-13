from run import app, db
from flask import render_template, url_for, flash, redirect, request
from models import Recipe, User
from forms import AddRecipeForm, UserRegistrationForm, UserLoginForm
import requests
from flask import jsonify


access_token = None
refresh_token = None

mocked_recipes = [
		{
			"Contents": "Spagetti", 
			"Details": "Easy to make", 
			"Name": "recipe_1", 
			"PostTime": "2011-10-13 13:33:13", 
			"Score": 3.0, 
			"Uid": 0, 
			"Views": 3
		},
		{
			"Contents": "Riceball", 
			"Details": "Put some eggs", 
			"Name": "recipe_2", 
			"PostTime": "2011-10-13 13:33:13", 
			"Score": 4.0, 
			"Uid": 1, 
			"Views": 4
		}        
	]

			 
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
		print(response.json())
		
		# flash('Recipe Added.', 'success')
		return redirect(url_for('allrecipes'))
	else:	
		return render_template('addrecipe.html', form=form, title="Add Recipe")


@app.route("/allrecipes")
def allrecipes():
	recipes = Recipe.query.all()
	return render_template('allrecipes.html', recipes=recipes, title="All Recipes")
	# return render_template('showrecipes.html', recipes=mocked_recipes)


@app.route("/myrecipes")
def myrecipes():
	my_recipes = Recipe.query.filter_by(user_id=current_user.id)
	return render_template('myrecipes.html', recipes=my_recipes, title="My Recipes")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	'''
	if current_user.is_authenticated:
		return redirect(url_for('myrecipes'))
	
	else:
	'''
	form = UserRegistrationForm()
	if form.validate_on_submit():
		# hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, password=form.password.data)
		print(user)
		db.session.add(user)
		db.session.commit()
		flash('{} adli hesap olusturuldu.'.format(form.username.data), 'success')
		return redirect(url_for('login'))
	else:
		return render_template('signup.html', title='Sign up', form=form)


# Don't change it's name. to trigger @login_required decorator, it needs to be named as login. 
@app.route("/", methods=['GET', 'POST'])
def login():
	global access_token
	global refresh_token

	form = UserLoginForm()
	if form.validate_on_submit():
		_json = {
			'username': form.username.data,
			'password': form.password.data
		}
		response = requests.post(url='http://localhost:5000/loginnn', params=_json)
		response_code = response.status_code
		response_json = response.json()
		access_token = response_json['access_token']
		refresh_token = response_json['refresh_token']

		next_page = request.args.get('next')
		return redirect(next_page) if next_page else redirect(url_for('allrecipes'))
	else:
		return render_template('signin.html', title='Sign in', form=form)


@app.route("/signout")
def signout():
	logout_user()
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
