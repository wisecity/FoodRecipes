from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class FoodRecipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, title):
        self.title = title

    def json(self):
        return {'Title': self.title}

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    def save_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_(self):
        db.session.delete(self)
        db.session.commit()
