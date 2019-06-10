from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'USER'
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(60), unique=True, nullable=False)
    Password = db.Column(db.String(60), nullable=False)

    def __init__(self, Username, Password):
        self.Username = Username
        self.Password = Password

    def json(self):
        return {'User Name': self.Username, "Id" : self.Id}

    @classmethod
    def find_by_Id(cls, Id):
        return cls.query.filter_by(Id=Id).first()

    def find_by_username(cls, Username):
        return cls.query.filter_by(Username=Username).first()

    def create_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_by_Id(cls, Id):
        cls.query.filter_by(Id=Id).delete()
        db.session.commit()

    def delete_by_Username(cls, Username):
        cls.query.filter_by(Username=Username).delete()
        db.session.commit()

    def update_(self, cls):
        _user = cls.query.filter_by(Id=self.Id).first()
        _user.Username = self.Username
        _user.Password = self.Password
        db.session.commit()

    def get_recipe_list(self):
        _user = User.query.filter_by(Id=self.Id).first()
        recipeList = Recipe.query.filter_by(Uid = _user.Id).all()
        return recipeList



class Recipe(db.Model):
    __tablename__ = 'RECIPE'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    PostTime = db.Column(db.DateTime, default=datetime.utcnow)
    Contents = db.Column(db.Text)
    Details = db.Column(db.Text)
    Views = db.Column(db.Integer)
    Score = db.Column(db.Float)
    Uid = db.Column(db.Integer, db.ForeignKey('USER.Id'), nullable=False)

    def __init__(self, Name, PostTime, Contents, Details, Views, Score, Uid):
        self.Name = Name
        self.PostTime = PostTime
        self.Contents = Contents
        self.Details = Details
        self.Views = Views
        self.Score = Score
        self.Uid = Uid

    def json(self):
        return {'Name': self.Name, "PostTime" : str(self.PostTime), "Contents" : self.Contents, "Details" : self.Details, "Views" : self.Views, "Score" : self.Score, "Uid" : self.Uid}

    @classmethod
    def find_by_Id(cls, Id):
        return cls.query.filter_by(Id=Id).first()

    def find_by_name(cls, recipeName):
        return cls.query.filter_by(Name=recipeName).first()

    def create_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_by_Id(cls, Id):
        cls.query.filter_by(Id=Id).delete()
        db.session.commit()

    def delete_by_Name(cls, Name):
        cls.query.filter_by(Name=Name).delete()
        db.session.commit()

    def update_(self, cls):
        _recipe = cls.query.filter_by(Id=self.Id).first()
        _recipe.Name = self.Name
        _recipe.PostTime = self.PostTime
        _recipe.Contents = self.Contents
        _recipe.Details = self.Details
        _recipe.Views = self.Views
        _recipe.Score = self.Score
        _recipe.Uid = self.Uid
        db.session.commit()

    def add_recipe(self, Username):
        _user = User.query.filter_by(Username=Username).first()
        self.Uid = _user.Id
        db.session.add(self)
        db.session.commit()

    def delete_recipe(self, Username):
        _user = User.query.filter_by(Username=Username).first()
        Recipe.query.filter_by(Uid = _user.Id, Id = self.Id).delete()
        db.session.commit()

    def edit_recipe(self, Username):
        _user = User.query.filter_by(Username=Username).first()
        _recipe = Recipe.query.filter_by(Uid = _user.Id, Id = self.Id)
        _recipe.Name = self.Name
        _recipe.PostTime = self.PostTime
        _recipe.Contents = self.Contents
        _recipe.Details = self.Details
        _recipe.Views = self.Views
        _recipe.Score = self.Score
        _recipe.Uid = self.Uid
        db.session.commit()

    def increase_view(self):
        self.Views = self.Views + 1
        db.session.commit()

    class Ingredient_Photos(db.Model):
        __tablename__ = 'INGREDIENT_PHOTOS'
        Id = db.Column(db.Integer, primary_key=True)
        Rid = db.Column(db.Integer, db.ForeignKey('RECIPE.Id'), nullable=False)
        Photo_Location = db.Column(db.String(100))

        def __init__(self, Rid, Photo_Location):
            self.Rid = Rid
            self.Photo_Location = Photo_Location

        @classmethod
        def add_photo(self, Name, Username):
            _user = User.query.filter_by(Username=Username).first()
            _recipe = Recipe.query.filter_by(Uid = _user.Id, Name=Name)
            self.Rid = _recipe.Id
            db.session.add(self)
            db.session.commit()

        def delete_photo(self, Name, Username):
            _user = User.query.filter_by(Username=Username).first()
            _recipe = Recipe.query.filter_by(Uid = _user.Id, Name=Name)
            Ingredient_Photos.query.filter_by(Rid = _recipe.Id, Id = self.Id).delete()
            db.session.commit()
    class Step_Photos(db.Model):
        __tablename__ = 'STEP_PHOTOS'
        Id = db.Column(db.Integer, primary_key=True)
        Rid = db.Column(db.Integer, db.ForeignKey('RECIPE.Id'), nullable=False)
        Photo_Location = db.Column(db.String(100))

        def __init__(self, Rid, Photo_Location):
            self.Rid = Rid
            self.Photo_Location = Photo_Location

        @classmethod
        def add_photo(self, Name, Username):
            _user = User.query.filter_by(Username=Username).first()
            _recipe = Recipe.query.filter_by(Uid = _user.Id, Name=Name)
            self.Rid = _recipe.Id
            db.session.add(self)
            db.session.commit()

        def delete_photo(self, Name, Username):
            _user = User.query.filter_by(Username=Username).first()
            _recipe = Recipe.query.filter_by(Uid = _user.Id, Name=Name)
            Step_Photos.query.filter_by(Rid = _recipe.Id, Id = self.Id).delete()
            db.session.commit()

    class Final_Photos(db.Model):
        __tablename__ = 'FINAL_PHOTOS'
        Id = db.Column(db.Integer, primary_key=True)
        Rid = db.Column(db.Integer, db.ForeignKey('RECIPE.Id'), nullable=False)
        Photo_Location = db.Column(db.String(100))

        def __init__(self, Rid, Photo_Location):
            self.Rid = Rid
            self.Photo_Location = Photo_Location

        @classmethod
        def add_photo(self, Name, Username):
            _user = User.query.filter_by(Username=Username).first()
            _recipe = Recipe.query.filter_by(Uid = _user.Id, Name=Name)
            self.Rid = _recipe.Id
            db.session.add(self)
            db.session.commit()

        def delete_photo(self, Name, Username):
            _user = User.query.filter_by(Username=Username).first()
            _recipe = Recipe.query.filter_by(Uid = _user.Id, Name=Name)
            Final_Photos.query.filter_by(Rid = _recipe.Id, Id = self.Id).delete()
            db.session.commit()
