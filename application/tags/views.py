from flask import redirect,render_template, request, url_for, abort
from application import app, db
from flask_login import current_user

from application.recipes.models import Recipe
from application.ingredients.models import Ingredient
from application.tags.models import Tag
from application.auth.models import User
from application.tags.forms import TagForm
from sqlalchemy.sql import text

#Index
@app.route("/tags", methods=["GET"])
def tags_index():
    statement = "SELECT tag.id,tag.name, COUNT(tag_id) AS count FROM tag,tags WHERE tag.id = tags.tag_id GROUP BY tag.name, tag.id"
    query = db.engine.execute(statement)
    return render_template("tags/list.html", tags=query)

#CREATE
#Only admins can create tags without recipes
@app.route("/recipes/new/", methods=["GET"])
def tag_createform():
    if current_user.get_role() != 'admin':
        return abort(401)
    return render_template("tags/new.html", form=TagForm())

@app.route("/tags", methods=["POST"])
def tag_create():
    if current_user.get_role() != 'admin':
        return abort(401)
  
    form = TagForm(request.form)
    if not form.validate():
        return render_template("tags/new.html", form=form)

    name = form.name.data.strip()
    newTag = Tag(name.capitalize())
    newTag.description = form.description.data

    db.session().add(newTag)
    db.session().commit()

    return redirect(url_for("tags_index"))

#READ
@app.route("/tags/<tag_id>/", methods=["GET"])
def tag_info(tag_id):
    tag = Tag.query.get(tag_id)
    recipes = Tag.find_recipes_with_tag(tag)
    return render_template("tags/tag.html", tag=tag, recipes=recipes)

#UPDATE
#Form for updating
@app.route("/tags/<tag_id>/edit/", methods=["GET"])
def tag_editform(tag_id):
    fetched_tag = Tag.query.get(tag_id)

    return render_template("tags/edit.html", tag=fetched_tag, form=TagForm())

#Actual updating
@app.route("/tags/<tag_id>/", methods=["POST"])
def tag_edit(tag_id):
    #POST is not accepted if current user is not an administrator
    if current_user.get_role() != 'admin':
        return abort(401)

    editedTag = Tag.query.get(tag_id)
    form = TagForm(request.form)

    if not form.validate():
        faultyTag = Tag(request.form['name'])
        faultyTag.id = tag_id
        faultyTag.description = Tag(request.form['description'])
        return render_template("tags/edit.html", form=TagForm(), tag=faultyTag)

    name = form.name.data.strip()
    editedTag.name = name.capitalize()
    editedTag.description = form.description.data

    db.session().commit()

    return redirect(url_for("tags_index"))

#DELETE
@app.route("/tags/<tag_id>/delete/", methods=["POST"])
def tag_delete(tag_id):
    if current_user.get_role() != 'admin':
        return abort(401)

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for("tags_index"))

#Detach recipe from tag
@app.route("/tags/<tag_id>/detach/<recipe_id>", methods=["POST"])
def detach_recipe(tag_id, recipe_id):
    if current_user.get_role() != 'admin':
        return abort(401)
    Tag.detach_recipe(tag_id, recipe_id)
    return redirect(url_for("tags_index"))

    

