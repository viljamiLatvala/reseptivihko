from flask import render_template
from application import app, db

from application.recipes.models import Recipe, Ingredient
from application.tags.models import Tag
from application.auth.models import User
from application.recipes.forms import RecipeForm

from sqlalchemy.sql import text

@app.route("/tags", methods=["GET"])
def tags_index():
    statement = "SELECT tag.id,tag.name, COUNT(tag_id) AS count FROM tag,tags WHERE tag.id = tags.tag_id GROUP BY tag.name, tag.id"
    query = db.engine.execute(statement)
    return render_template("tags/list.html", tags = query)

#Individual tag view listing recipes associated with it
@app.route("/tags/<tag_id>/", methods=["GET"])
def tag_info(tag_id):
    tag = Tag.query.get(tag_id)
    recipes = Tag.find_recipes_with_tag(tag)
    return render_template("tags/tag.html", tag = tag, recipes = recipes)
