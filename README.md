To run: inside FoodRecipes directory, python run.py
To stop: ctrl + c on linux
When debugger mode is active, you don't need to stop the application.


db: sqlAlchemy
At fresh start, do the db.drop_all() thing.

Debugging
inside the FoodRecipes directory:

> python
> from foodrecipes import db
> from foodrecipes.models import User

> db.drop_all()		# to drop all relations
> db.create_all()	

> user = User(username='Doruk', password='dodo1234')
> db.session.add(user)
> db.session.commit()

> db.session.query(User).first().password


