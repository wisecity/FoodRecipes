from run import app, db
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from models import Recipe, User
from forms import AddRecipeForm, UserRegistrationForm, UserLoginForm



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
		recipe = Recipe(name=form.name.data, contents=form.contents.data, 
			details=form.details.data)
		recipe.add_recipe(username="User_1")
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


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    else:
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
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    else:
        form = UserLoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            # if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user: 
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('account'))
            else:
                flash('Giris basarisiz.', 'danger')
        else:
            return render_template('signin.html', title='Sign in', form=form)


@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('mainpage'))


@app.route("/account")
@login_required
def account():
    return render_template("account.html")