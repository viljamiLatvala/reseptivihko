from flask import redirect,render_template, request, url_for, abort
from flask_login import current_user, login_required
from application import app, db

from application.recipes.models import Recipe, Tag, Ingredient
from application.auth.models import User
from application.recipes.forms import RecipeForm, RecipeEditForm

from sqlalchemy.sql import text
#Tag routes to be moved into their own respective folder
##List of tags
@app.route("/tags", methods=["GET"])
def tags_index():
    statement = "SELECT tag.id,tag.name, COUNT(tag_id) AS count FROM tag,tags WHERE tag.id = tags.tag_id GROUP BY tag.name"
    query = db.engine.execute(statement)
    return render_template("tags/list.html", tags = query)

##Individual tag view listing recipes associated with it
@app.route("/tags/<tag_id>/", methods=["GET"])
def tag_info(tag_id):
    tag = Tag.query.get(tag_id)
    recipes = find_recipes_with_tag(tag)
    return render_template("tags/tag.html", tag = tag, recipes = recipes)

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
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id)
    return render_template("recipes/recipe.html", recipe = recipe, recipeCreator = recipeCreator, tags = tags, ingredients = ingredients)

##Form for editing specific recipe
@app.route("/recipes/<recipe_id>/edit/", methods=["GET"])
def recipe_editform(recipe_id):
    fetched_recipe = Recipe.query.get(recipe_id)
    fetched_tags = find_recipe_tags(fetched_recipe)
    joined_tags = ""
    for tag in fetched_tags:
        joined_tags += tag[1]
        joined_tags += ","

    fetched_ingredients = find_recipe_ingredients(fetched_recipe)
    joined_ingredients = ""
    for ingredient in fetched_ingredients:
        joined_ingredients += ingredient.line + "\n"

    return render_template("recipes/edit.html", recipe = fetched_recipe, form = RecipeEditForm(), tags = joined_tags, ingredients = joined_ingredients)

##Route for deleting a recipe
@app.route("/recipes/<recipe_id>/delete/", methods=["POST"])
def recipe_delete(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if (recipe.account_id is not current_user.get_id()) and (current_user.get_role() != 'admin'):
        return abort(401)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("recipes_index"))

##Route for editing a recipe
@app.route("/recipes/<recipe_id>/", methods=["POST"])
def recipe_edit(recipe_id):
    
    recipe = Recipe.query.get(recipe_id)
    if (recipe.account_id is not current_user.get_id()) and (current_user.get_role() != 'admin'):
        return abort(401)

    form = RecipeEditForm(request.form)
    tags = form.tags.data.split(',')

    if not form.validate():
        faultyRecipe = Recipe(request.form['name'])
        faultyRecipe.id = recipe_id
        faultyRecipe.instruction = request.form['instruction']
        faultyRecipe.preptime = request.form.get("preptime")
        faultyIngredients = request.form.get("ingredients")
        faultyTags = request.form.get("tags")
        return render_template("recipes/edit.html", recipe = faultyRecipe, form = form, tags = faultyTags, ingredients = faultyIngredients)

    r = Recipe.query.get(recipe_id)
    r.name = request.form.get("name")
    r.instruction = request.form.get("instruction")
    r.preptime = request.form.get("preptime")

    add_tags(tags, r)

    db.session().commit()

    ingredients = request.form.get("ingredients").splitlines()
    add_ingredients(ingredients, r)
    

    return redirect(url_for("recipes_index"))

##Route for adding a new recipe
@app.route("/recipes/", methods=["POST"])
def recipes_create():
    form = RecipeForm(request.form)
    tagsString = form.tags.data.strip()
    tags = tagsString.split(',')
    ingredients = form.ingredients.data.splitlines()

    if not form.validate():
        return render_template("recipes/new.html", form = form)

    r = Recipe(form.name.data)
    r.instruction = form.instruction.data
    r.preptime = form.preptime.data
    r.account_id = current_user.id
    add_tags(tags, r)
    db.session().add(r)
    db.session().commit()

    addedRecipe = Recipe.query.filter(Recipe.name == r.name).first()
    add_ingredients(ingredients, addedRecipe)

    return redirect(url_for("recipes_index"))

#Helper functions and queries
def add_tags(tags, recipe):
    ## TAG DELETION DOES NOT WORK AND TAGS ARE CASE SENSITIVE
    for tag in tags:
        tag = tag.strip()
        if tag == "":
            continue
        tagExists = Tag.query.filter(Tag.name == tag).first()
        if tagExists:
            recipe.tags.append(tagExists)
        else:
            newTag = Tag(tag)
            recipe.tags.append(newTag)


def find_recipe_tags(recipe):
    statement = text("SELECT tag.id, tag.name FROM tag, recipe, tags"
                        " WHERE tag.id = tags.tag_id" 
                        " AND recipe.id = tags.recipe_id" 
                        " AND recipe.name = :name").params(name = recipe.name)
    query = db.engine.execute(statement)
    response = []
    for row in query:
        response.append(row)

    return response

def find_recipes_with_tag(tag):
    statement = text("SELECT recipe.id, recipe.name, recipe.preptime FROM recipe, tags, tag"
                        " WHERE tag.id = tags.tag_id" 
                        " AND recipe.id = tags.recipe_id"
                        " AND tag.name = :tag").params(tag = tag.name)
    query = db.engine.execute(statement)
    response = []
    for row in query:
        response.append(row)

    print(response)
    return response

def add_ingredients(ingredients, recipe):
    ##FIRST format recipe to have no ingredients
    find_recipe_ingredients(recipe).delete()

    for line in ingredients:
        ingredient = Ingredient(line, recipe.id)
        db.session.add(ingredient)
    db.session.commit()

def find_recipe_ingredients(recipe):
    ingredients = Ingredient.query.filter(Ingredient.recipe_id == recipe.id)
    return ingredients