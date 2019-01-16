from flask import redirect,render_template, request, url_for, abort
from flask_login import current_user, login_required
from application import app, db

from application.recipes.models import Recipe
from application.tags.models import Tag
from application.auth.models import User
from application.ingredients.models import Ingredient
from application.recipes.forms import RecipeForm, RecipeEditForm

from sqlalchemy.sql import text

#index
@app.route("/recipes/", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes=Recipe.query.all())

#CREATE
#Form for creation
@app.route("/recipes/new/", methods=["GET"])
@login_required
def recipes_form():
    return render_template("recipes/new.html", form=RecipeForm())

#Actual creation
@app.route("/recipes/", methods=["POST"])
def recipes_create():

    form = RecipeForm(request.form)
    form.recipe_id = -1
    #Checking that the form passes validations
    if not form.validate():
        return render_template("recipes/new.html", form=form)

    #Adding the new recipe
    name = form.name.data.strip()
    name = (name[0].upper() + name[1:])
    newRecipe = Recipe(name)
    newRecipe.instruction = form.instruction.data
    newRecipe.preptime = form.preptime.data
    newRecipe.account_id = current_user.id

    #Separating and adding tags
    tagsString = form.tags.data.strip()
    tags = tagsString.split(',')
    Tag.add_tags(tags, newRecipe)

    #Commiting changes
    db.session().add(newRecipe)
    db.session().commit()
    
    #Ingredients need recipe ID, so they are added only after the recipe is added
    addedRecipe = Recipe.query.filter(Recipe.name == newRecipe.name).first()
    ingredients = form.ingredients.data.splitlines()
    Ingredient.add_ingredients(ingredients, addedRecipe)

    return redirect(url_for("recipes_index"))

#READ
@app.route("/recipes/<recipe_id>/", methods=["GET"])
def recipe_info(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    tags = Recipe.find_recipe_tags(recipe)
    recipeCreator = User.query.filter_by(id=recipe.account_id).first();
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id)
    return render_template("recipes/recipe.html", recipe=recipe, recipeCreator=recipeCreator, tags=tags, ingredients=ingredients)

#UPDATE
#Form for updating
@app.route("/recipes/<recipe_id>/edit/", methods=["GET"])
def recipe_editform(recipe_id):
    fetched_recipe = Recipe.query.get(recipe_id)
    fetched_tags = Recipe.find_recipe_tags(fetched_recipe)
    joined_tags = ""

    tags_length = len(fetched_tags)
    for i in range(tags_length):
        joined_tags += fetched_tags[i][1]
        if i < tags_length-1:
            joined_tags += ', '

    fetched_ingredients = Ingredient.find_recipe_ingredients(fetched_recipe)
    joined_ingredients = ""
    for ingredient in fetched_ingredients:
        joined_ingredients += ingredient.line + "\n"

    return render_template("recipes/edit.html", recipe=fetched_recipe, form=RecipeEditForm(), tags=joined_tags, ingredients=joined_ingredients)

#Actual updating
@app.route("/recipes/<recipe_id>/", methods=["POST"])
def recipe_edit(recipe_id):
    
    #POST is not accepted if current user is not the creator of the recipe or an administrator
    recipe = Recipe.query.get(recipe_id)
    if (recipe.account_id is not current_user.get_id()) and (current_user.get_role() != 'admin'):
        return abort(401)

    form = RecipeEditForm(request.form)

    #If form does not pass validations, a new, faulty form is created to be shown along with error messages, but never put to the database
    if not form.validate():
        faultyRecipe = Recipe(request.form['name'])
        faultyRecipe.id = recipe_id
        faultyRecipe.instruction = request.form['instruction']
        faultyRecipe.preptime = request.form.get("preptime")
        faultyIngredients = request.form.get("ingredients")
        faultyTags = request.form.get("tags")
        return render_template("recipes/edit.html", recipe=faultyRecipe, form=form, tags=faultyTags, ingredients=faultyIngredients)

    #Fetching and editing the recipe
    changedRecipe = Recipe.query.get(recipe_id)
    name = request.form.get("name").strip()
    name = name[0].upper() + name[1:]
    changedRecipe.name = name
    changedRecipe.instruction = request.form.get("instruction")
    changedRecipe.preptime = request.form.get("preptime")

    #Add tags for the recipe
    tags = form.tags.data.split(',')
    Tag.add_tags(tags, changedRecipe)

    db.session().commit()

    ingredients = request.form.get("ingredients").splitlines()
    Ingredient.add_ingredients(ingredients, changedRecipe)

    return redirect(url_for("recipes_index"))

#DELETE
@app.route("/recipes/<recipe_id>/delete/", methods=["POST"])
def recipe_delete(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if (recipe.account_id is not current_user.get_id()) and (current_user.get_role() != 'admin'):
        return abort(401)
    Ingredient.find_recipe_ingredients(recipe).delete()
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("recipes_index"))

