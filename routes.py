from flask import render_template, url_for, flash, redirect, request
# from flask_login import login_user, current_user, logout_user, login_required
from base import Recipe
from forms import AddRecipeForm
from app import app


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
		# Hacked it, waiting for api.
		recipe = Recipe(Name=form.name.data, Contents=form.contents.data, 
			Details=form.details.data)
		recipe.add_recipe(Username="User_1")
		flash('Recipe Added.', 'success')
		return redirect(url_for('mainpage'))
	else:	
		return render_template('addrecipe.html', form=form)


@app.route("/showrecipes")
def showrecipes():
	recipes = Recipe.query.all()
	return render_template('showrecipes.html', recipes=recipes)
	# return render_template('showrecipes.html', recipes=mocked_recipes)


@app.route("/mainpage")
def mainpage():
	return render_template('mainpage.html')
