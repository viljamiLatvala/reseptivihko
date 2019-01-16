
from application import db
from sqlalchemy.sql import text
from application.recipes.models import Recipe, tags


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144), nullable=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def tags_summary():
        statement = text("SELECT tag.id, tag.name, COUNT(tag_id) AS count"
                         " FROM tag LEFT JOIN tags ON tags.tag_id = tag.id"
                         " GROUP BY tag.name ORDER BY COUNT(tag_id) DESC")
        query = db.engine.execute(statement)
        return query

    @staticmethod
    def find_recipes_with_tag(tag):
        statement = text("SELECT recipe.id, recipe.name, recipe.preptime FROM"
                         " recipe, tags, tag"
                         " WHERE tag.id = tags.tag_id"
                         " AND recipe.id = tags.recipe_id"
                         " AND tag.id = :tag").params(tag=tag.id)
        query = db.engine.execute(statement)
        response = []
        for row in query:
            response.append(row)

        print(response)
        return response

    @staticmethod
    def add_tags(tags, recipe):
        prev_tags = Recipe.find_recipe_tags(recipe)
        for tag in prev_tags:
            rmtag = Tag.query.filter(Tag.id == tag[0]).first()
            recipe.tags.remove(rmtag)

        for tag in tags:
            if tag == "":
                break
            # Format tags to obey following rules:
            # no leading or trailing whitespace
            # capitalized, otherwise lowercase
            tag = tag.strip().lower().capitalize()

            tagExists = Tag.query.filter(Tag.name == tag).first()
            if tagExists:
                recipe.tags.append(tagExists)
            else:
                newTag = Tag(tag)
                recipe.tags.append(newTag)

    @staticmethod
    def detach_recipe(tag_id, recipe_id):
        detach_statement = text("DELETE FROM tags WHERE tag_id = :tag_id"
                                " AND recipe_id = :recipe_id"
                                ).params(recipe_id=recipe_id, tag_id=tag_id)
        db.engine.execute(detach_statement)
        tags_check = text("SELECT COUNT(*) AS count FROM tag,tags"
                          " WHERE tag.id=tags.tag_id AND"
                          " tag.id=:tag_id"
                          ).params(tag_id=tag_id)
        check_result = db.engine.execute(tags_check)
        if check_result.first()[0] == 0:
            print("POISTETAAN")
            tag_to_rm = Tag.query.filter(Tag.id == tag_id).first()
            db.session.delete(tag_to_rm)
            db.session.commit()
