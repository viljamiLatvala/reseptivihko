from application import db
from application.models import Base
from sqlalchemy.sql import text

# Junction table for Recipe and Tag
tags = db.Table('tags',
                db.Column('tag_id',
                          db.Integer,
                          db.ForeignKey('tag.id'),
                          primary_key=True
                          ),
                db.Column('recipe_id',
                          db.Integer,
                          db.ForeignKey('recipe.id'),
                          primary_key=True
                          )
                )


class Recipe(Base):
    name = db.Column(db.String(144), nullable=False)
    instruction = db.Column(db.String(6000))
    preptime = db.Column(db.Integer)
    account_id = db.Column(db.Integer,
                           db.ForeignKey('account.id'),
                           nullable=False
                           )
    tags = db.relationship('Tag',
                           secondary=tags,
                           lazy='subquery',
                           backref=db.backref('recipes', lazy=True)
                           )

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find_recipe_tags(recipe):
        statement = text("SELECT tag.id, tag.name FROM tag, recipe, tags"
                         " WHERE tag.id = tags.tag_id"
                         " AND recipe.id = tags.recipe_id"
                         " AND recipe.id= :id").params(id=recipe.id)
        query = db.engine.execute(statement)
        response = []
        for row in query:
            response.append(row)

        return response

    @staticmethod
    def summary():
        statement = text("SELECT COUNT(recipe.id),"
                         " COALESCE (AVG(recipe.preptime),0),"
                         " COUNT(DISTINCT account_id)"
                         " FROM recipe")
        query = db.engine.execute(statement)
        result = []
        for row in query:
            result = row

        return result
