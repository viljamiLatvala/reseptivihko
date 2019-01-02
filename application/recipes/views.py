from application import app, db
from flask import redirect,render_template, request, url_for
from application.recipes.models import Recipe
from application.recipes.forms import RecipeForm, RecipeEditForm
from flask_login import login_required, current_user

@app.route("/recipes", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes = Recipe.query.all())

@app.route("/recipes/new/")
@login_required
def recipes_form():
    return render_template("recipes/new.html", form = RecipeForm())

@app.route("/recipes/<recipe_id>/", methods=["GET"])
def recipe_info(recipe_id):
    return render_template("recipes/recipe.html", recipe = Recipe.query.get(recipe_id))

@app.route("/recipes/<recipe_id>/edit/", methods=["GET"])
@login_required
def recipe_editform(recipe_id):
    return render_template("recipes/edit.html", recipe = Recipe.query.get(recipe_id), form = RecipeEditForm())

@app.route("/recipes/<recipe_id>/delete/", methods=["POST"])
@login_required
def recipe_delete(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("recipes_index"))

@app.route("/recipes/<recipe_id>/", methods=["POST"])
@login_required
def recipe_edit(recipe_id):
    form = RecipeEditForm(request.form)

    if not form.validate():
        faultyRecipe = Recipe(request.form['name'])
        faultyRecipe.id = recipe_id
        faultyRecipe.instruction = request.form['instruction']
        return render_template("recipes/edit.html", recipe = faultyRecipe, form = form)

    r = Recipe.query.get(recipe_id)
    r.name = request.form.get("name")
    r.instruction = request.form.get("instruction")

    db.session().commit()

    return redirect(url_for("recipes_index"))

@app.route("/recipes/", methods=["POST"])
@login_required
def recipes_create():
    form = RecipeForm(request.form)

    if not form.validate():
        return render_template("recipes/new.html", form = form)

    r = Recipe(form.name.data)
    r.instruction = form.instruction.data
    r.account_id = current_user.id
    db.session().add(r)
    db.session().commit()

    return redirect(url_for("recipes_index"))