from flask import redirect,render_template, request, url_for, abort
from flask_login import current_user, login_required
from application import app, db

from application.recipes.models import Recipe, Ingredient
from application.tags.models import Tag
from application.auth.models import User
from application.recipes.forms import RecipeForm, RecipeEditForm

from sqlalchemy.sql import text

#List of all recipes
@app.route("/recipes", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes = Recipe.query.all())

#Form for adding new recipes
@app.route("/recipes/new/")
@login_required
def recipes_form():
    return render_template("recipes/new.html", form = RecipeForm())

#Individual recipe view
@app.route("/recipes/<recipe_id>/", methods=["GET"])
def recipe_info(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    tags = Recipe.find_recipe_tags(recipe)
    recipeCreator = User.query.filter_by(id=recipe.account_id).first();
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id)
    return render_template("recipes/recipe.html", recipe = recipe, recipeCreator = recipeCreator, tags = tags, ingredients = ingredients)

#Form for editing specific recipe
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

    fetched_ingredients = find_recipe_ingredients(fetched_recipe)
    joined_ingredients = ""
    for ingredient in fetched_ingredients:
        joined_ingredients += ingredient.line + "\n"

    return render_template("recipes/edit.html", recipe = fetched_recipe, form = RecipeEditForm(), tags = joined_tags, ingredients = joined_ingredients)

#Route for deleting a recipe
@app.route("/recipes/<recipe_id>/delete/", methods=["POST"])
def recipe_delete(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if (recipe.account_id is not current_user.get_id()) and (current_user.get_role() != 'admin'):
        return abort(401)
    find_recipe_ingredients(recipe).delete()
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("recipes_index"))

#Route for editing a recipe
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
        return render_template("recipes/edit.html", recipe = faultyRecipe, form = form, tags = faultyTags, ingredients = faultyIngredients)

    #Fetching and editing the recipe
    changedRecipe = Recipe.query.get(recipe_id)
    name = request.form.get("name").strip()
    name = name[0].upper() + name[1:]
    changedRecipe.name = name
    changedRecipe.instruction = request.form.get("instruction")
    changedRecipe.preptime = request.form.get("preptime")

    #Add tags for the recipe
    tags = form.tags.data.split(',')
    add_tags(tags, changedRecipe)

    db.session().commit()

    ingredients = request.form.get("ingredients").splitlines()
    add_ingredients(ingredients, changedRecipe)

    return redirect(url_for("recipes_index"))

#Route for adding a new recipe
@app.route("/recipes/", methods=["POST"])
def recipes_create():

    form = RecipeForm(request.form)
    form.recipe_id = -1
#Checking that the form passes validations
    if not form.validate():
        return render_template("recipes/new.html", form = form)

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
    add_tags(tags, newRecipe)

#Commiting changes
    db.session().add(newRecipe)
    db.session().commit()
    
#Ingredients need recipe ID, so they are added only after the recipe is added
    addedRecipe = Recipe.query.filter(Recipe.name == newRecipe.name).first()
    ingredients = form.ingredients.data.splitlines()
    add_ingredients(ingredients, addedRecipe)

    return redirect(url_for("recipes_index"))

#Helper functions and queries
def add_tags(tags, recipe):
    prev_tags = Recipe.find_recipe_tags(recipe)
    for tag in prev_tags:
        rmtag = Tag.query.filter(Tag.id == tag[0]).first()
        recipe.tags.remove(rmtag)

    for tag in tags:
        if tag == "":
            break
        #Format tags to obey following rules:
        #no leading or trailing whitespace
        #capitalized, otherwise lowercase
        tag = tag.strip().lower().capitalize()

        tagExists = Tag.query.filter(Tag.name == tag).first()
        if tagExists:
            recipe.tags.append(tagExists)
        else:
            newTag = Tag(tag)
            recipe.tags.append(newTag)

def edit_tags(new_tags, recipe):
    prev_tags = Recipe.find_recipe_tags(recipe)

def add_ingredients(ingredients, recipe):
    #FIRST format recipe to have no ingredients
    find_recipe_ingredients(recipe).delete()

    for line in ingredients:
        line = line.strip()
        line = line[0].upper() + line[1:]
        ingredient = Ingredient(line, recipe.id)
        db.session.add(ingredient)
    db.session.commit()

def find_recipe_ingredients(recipe):
    ingredients = Ingredient.query.filter(Ingredient.recipe_id == recipe.id)
    return ingredients
