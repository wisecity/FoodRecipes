from flask import render_template, url_for, flash, redirect, request
from recipeweb import db, app, bcrypt
from recipeweb.forms import RegistrationForm, LoginForm, UpdateAccountForm, CommentForm
from recipeweb.models import User, Post, MainPageComments
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		'author': 'Doruk',
		'title': 'Olumsuzluk',
		'date': '22.04.1998'
	},
	{
		'author': 'Doruk',
		'title': 'Motorsiklet',
		'date': '20.05.2019'
	}
	
]


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		print(user)
		db.session.add(user)
		db.session.commit()
		flash('{} adli hesap olusturuldu.'.format(form.username.data), 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Kayit Ol', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Giris basarisiz.', 'danger')
	return render_template('login.html', title='Giris Yap', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Hesap guncellendi.', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='Account', form=form)


@app.route("/my_feed")
@login_required
def my_feed():
	posts = Post.query.filter_by(user_id=current_user.id)
	return render_template('my_feed.html', title='My Feed', posts=posts)


@app.route("/feed")
@login_required
def feed():
	posts = Post.query.filter_by()
	return render_template('feed.html', title='Feed', posts=posts)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
	comments = db.session.query(MainPageComments).order_by(MainPageComments.date_posted)
	form = CommentForm()
	if form.validate_on_submit():
		if form.author.data == "":
			form.author.data = "Anonim"
		comment = MainPageComments(content=form.content.data, author=form.author.data)
		db.session.add(comment)
		db.session.commit()
		flash('Yorum eklendi.', 'success')
		return redirect(url_for('catch_all', path=path))

	return render_template('{}.html'.format(path), form=form, comments=comments)



