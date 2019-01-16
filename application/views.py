from flask import render_template
from application import app

from application.recipes.models import Recipe


@app.route("/")
def index():
    return render_template("index.html", recipe_summary=Recipe.summary())
