from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'USER'
	Id = db.Column(db.Integer, primary_key=True)
	Username = db.Column(db.String(60), unique=True, nullable=False)
	Password = db.Column(db.String(60), nullable=False)

class Recipe(db.Model):
    __tablename__ = 'RECIPE'
    Id = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String(100), nullable=False)
    PostTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Contents = db.Column(db.Text)
    Views = db.Column(db.Integer)
    Score = db.Column(db.Float)
    Uid = db.Column(db.Integer, db.ForeignKey('USER.Id'), nullable=False)

    def __init__(self, Name, PostTime, Contents, Views, Score):
        self.Name = Name
        self.PostTime = PostTime
        self.Contents = Contents
        self.Views = Views
        self.Score = Score

    def json(self):
        return {'Name': self.Name}

    @classmethod
    def find_by_name(cls, Name):
        return cls.query.filter_by(Name=Name).first()

    def save_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_(self):
        db.session.delete(self)
        db.session.commit()
