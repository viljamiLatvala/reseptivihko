
from application import db
from sqlalchemy.sql import text

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find_recipes_with_tag(tag):
        statement = text("SELECT recipe.id, recipe.name, recipe.preptime FROM recipe, tags, tag"
                            " WHERE tag.id = tags.tag_id" 
                            " AND recipe.id = tags.recipe_id"
                            " AND tag.id = :tag").params(tag = tag.id)
        query = db.engine.execute(statement)
        response = []
        for row in query:
            response.append(row)

        print(response)
        return response