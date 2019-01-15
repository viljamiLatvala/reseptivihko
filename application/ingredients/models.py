from application import db
from application.models import Base

class Ingredient(Base):
    line = db.Column(db.String(500), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __init__(self, line, recipe_id):
        self.line = line
        self.recipe_id = recipe_id
    
    @staticmethod
    def add_ingredients(ingredients, recipe):
        #FIRST format recipe to have no ingredients
        Ingredient.query.filter(Ingredient.recipe_id == recipe.id).delete()

        for line in ingredients:
            line = line.strip()
            line = line[0].upper() + line[1:]
            ingredient = Ingredient(line, recipe.id)
            db.session.add(ingredient)
        db.session.commit()

    @staticmethod
    def find_recipe_ingredients(recipe):
        return Ingredient.query.filter(Ingredient.recipe_id == recipe.id)