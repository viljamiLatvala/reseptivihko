from application import app, db
from flask import redirect,render_template, request, url_for, abort
from application.recipes.models import Recipe, Tag
from application.auth.models import User
from application.recipes.forms import RecipeForm, RecipeEditForm
from flask_login import login_required, current_user
from sqlalchemy.sql import text
#Tag routes to be moved into their own respective folder
##List of tags
@app.route("/tags", methods=["GET"])
def tags_index():
    return render_template("tags/list.html", tags = Tag.query.all())

##Individual tag view listing recipes associated with it
@app.route("/tags/<tag_id>/", methods=["GET"])
def tag_info(tag_id):
    return render_template("tags/tag.html")

#Recipe routes
##List of all recipes
@app.route("/recipes", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes = Recipe.query.all())

##Form for adding new recipes
@app.route("/recipes/new/")
@login_required
def recipes_form():
    return render_template("recipes/new.html", form = RecipeForm())

##Individual recipe view
@app.route("/recipes/<recipe_id>/", methods=["GET"])
def recipe_info(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    print(find_recipe_tags(recipe))
    tags = find_recipe_tags(recipe)
    recipeCreator = User.query.filter_by(id=recipe.account_id).first();
    return render_template("recipes/recipe.html", recipe = recipe, recipeCreator = recipeCreator, tags = tags)

##Form for editing specific recipe
@app.route("/recipes/<recipe_id>/edit/", methods=["GET"])
@login_required
def recipe_editform(recipe_id):
    return render_template("recipes/edit.html", recipe = Recipe.query.get(recipe_id), form = RecipeEditForm())

##Route for deleting a recipe
@app.route("/recipes/<recipe_id>/delete/", methods=["POST"])
@login_required
def recipe_delete(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe.account_id is not current_user.get_id():
        return abort(401)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("recipes_index"))

##Route for editing a recipe
@app.route("/recipes/<recipe_id>/", methods=["POST"])
@login_required
def recipe_edit(recipe_id):
    
    recipe = Recipe.query.get(recipe_id)
    if recipe.account_id is not current_user.get_id():
        return abort(401)

    form = RecipeEditForm(request.form)
    tags = form.tags.data.split(', ')

    if not form.validate():
        faultyRecipe = Recipe(request.form['name'])
        faultyRecipe.id = recipe_id
        faultyRecipe.instruction = request.form['instruction']
        return render_template("recipes/edit.html", recipe = faultyRecipe, form = form)

    r = Recipe.query.get(recipe_id)
    r.name = request.form.get("name")
    r.instruction = request.form.get("instruction")

    add_tags(tags, r)

    db.session().commit()

    return redirect(url_for("recipes_index"))

##Route for adding a new recipe
@app.route("/recipes/", methods=["POST"])
@login_required
def recipes_create():
    form = RecipeForm(request.form)
    tags = form.tags.data.split(', ')

    if not form.validate():
        return render_template("recipes/new.html", form = form)

    r = Recipe(form.name.data)
    r.instruction = form.instruction.data
    r.account_id = current_user.id

    add_tags(tags, r)

    db.session().add(r)
    db.session().commit()

    return redirect(url_for("recipes_index"))

#Helper functions
def add_tags(tags, recipe):
     for tag in tags:
        tagExists = Tag.query.filter(Tag.name == tag).first()
        if tagExists:
            recipe.tags.append(tagExists)
        else:
            newTag = Tag(tag)
            recipe.tags.append(newTag)


def find_recipe_tags(recipe):
    print("ID:", recipe.id)
    statement = text("SELECT tag.name FROM tag, recipe, tags"
                        " WHERE tag.id = tags.tag_id" 
                        " AND recipe.id = tags.recipe_id" 
                        " AND recipe.name = :name").params(name = recipe.name)
    query = db.engine.execute(statement)
    response = []
    for row in query:
        response.append(row[0])

    return response