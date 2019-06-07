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
        return {'User Name': self.Username}
        
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

    def update_(cls, self):
        _user = cls.query.filter_by(Id=self.Id).first()        
        _user.Username = self.Username
        _user.Password = self.Password        
        db.session.commit()

class Recipe(db.Model):
    __tablename__ = 'RECIPE'
    Id = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String(100), unique=True, nullable=False)
    PostTime = db.Column(db.DateTime, default=datetime.utcnow)
    Contents = db.Column(db.Text)
    Views = db.Column(db.Integer)
    Score = db.Column(db.Float)
    Uid = db.Column(db.Integer, db.ForeignKey('USER.Id'), nullable=False)

    def __init__(self, Name, PostTime, Contents, Views, Score, Uid):
        self.Name = Name
        self.PostTime = PostTime
        self.Contents = Contents
        self.Views = Views
        self.Score = Score
        self.Uid = Uid

    def json(self):
        return {'Name': self.Name}

    @classmethod
    def find_by_Id(cls, Id):
        return cls.query.filter_by(Id=Id).first()

    def find_by_name(cls, Name):
        return cls.query.filter_by(Name=Name).first()

    def create_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_by_Id(cls, Id):
        cls.query.filter_by(Id=Id).delete()
        db.session.commit()

    def delete_by_Name(cls, Name):
        cls.query.filter_by(Name=Name).delete()
        db.session.commit()

    def update_(cls, self):
        _recipe = cls.query.filter_by(Id=self.Id).first()
        db.session.commit()
        _recipe.Name = self.Name
        _recipe.PostTime = self.PostTime
        _recipe.Contents = self.Contents
        _recipe.Views = self.Views
        _recipe.Score = self.Score
        _recipe.Uid = self.Uid
        db.session.commit()
