from application import db
from application.models import Base

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

class Recipe(Base):
    name = db.Column(db.String(144), nullable=False)
    introduction = db.Column(db.String(144))
    instruction = db.Column(db.String(6000))
    preptime = db.Column(db.Integer)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('recipes', lazy=True))

    def __init__(self, name):
        self.name = name
        
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)

    def __init__(self, name):
        self.name = name