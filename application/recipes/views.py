from application import app, db
from flask import redirect,render_template, request, url_for
from application.recipes.models import Recipe

@app.route("/recipes", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes = Recipe.query.all())

@app.route("/recipes/new/")
def recipes_form():
    return render_template("recipes/new.html")

@app.route("/recipes/<recipe_id>/", methods=["GET"])
def recipe_info(recipe_id):
    return render_template("recipes/recipe.html", recipe = Recipe.query.get(recipe_id))

@app.route("/recipes/<recipe_id>/edit/", methods=["GET"])
def recipe_editform(recipe_id):
    return render_template("recipes/edit.html", recipe = Recipe.query.get(recipe_id))

@app.route("/recipes/<recipe_id>/", methods=["POST"])
def recipe_edit(recipe_id):
    r = Recipe.query.get(recipe_id)
    r.name = request.form.get("name")
    r.instruction = request.form.get("instruction")

    db.session().commit()

    return redirect(url_for("recipes_index"))

@app.route("/recipes/", methods=["POST"])
def recipes_create():
    r = Recipe(request.form.get("name"))
    r.instruction = request.form.get("instruction")
    db.session().add(r)
    db.session().commit()

    return redirect(url_for("recipes_index"))