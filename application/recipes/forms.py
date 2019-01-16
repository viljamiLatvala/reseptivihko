from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField,\
                    HiddenField, validators, ValidationError
from application.recipes.models import Recipe


# Validators for checking tag length or ingredient line length
#  doesn't exeed set maximum lengths
def validate_tag_length(min=-1, max=-1):
    msg = 'Each tag must be between %d and %d characters long.' % (min, max)

    def _validate_tag_length(form, field):
        tags = field.data.split(',')

        map(str.strip, tags)
        if len(tags) == 1 and tags[0] == "":
            return _validate_tag_length

        for tag in tags:
            if len(tag) < min or max != -1 and len(tag) > max:
                raise ValidationError(msg)
                break
    return _validate_tag_length


def validate_ingredients_length(min=-1, max=-1):
    msg = ('Each ingredient line must be'
           ' between %d and %d characters long.' % (min, max))

    def _validate_ingredients_length(form, field):
        ingredients = field.data.splitlines()
        for line in ingredients:
            line = line.strip()
            if len(line) < min or max != -1 and len(line) > max:
                raise ValidationError(msg)
                break
    return _validate_ingredients_length


# Making sure recipe names are unique
def unique_name(action):
    message = 'Name must be unique!'

    def _unique_name(form, field):
        nameExists = Recipe.query.filter(Recipe.name == field.data).count()
        if action == 'new' and nameExists:
            raise ValidationError(message)
        elif action == 'edit' and nameExists:
            existing = Recipe.query.filter(Recipe.name == field.data).first()
            if int(existing.id) != int(form.recipeId.data):
                raise ValidationError(message)
    return _unique_name


# Form for creating a recipe
# Should validator maxes be inherited from models.py?
class RecipeForm(FlaskForm):
    name = StringField("Name",
                       [validators.Length(min=3, max=144),
                        unique_name(action='new')]
                       )
    ingredients = TextAreaField("Ingredients",
                                [validate_ingredients_length(min=3, max=500)]
                                )
    preptime = IntegerField("Preparation time (minutes)",
                            [validators.required()]
                            )
    instruction = TextAreaField("Instruction",
                                [validators.Length(min=10, max=6000)]
                                )
    tags = TextAreaField("Tags", [validate_tag_length(min=3, max=18)])

    class Meta:
        csrf = False


class RecipeEditForm(FlaskForm):
    recipeId = HiddenField("Id")
    name = StringField("Name",
                       [validators.Length(min=3, max=144),
                        unique_name(action='edit')]
                       )
    ingredients = TextAreaField("Ingredients",
                                [validate_ingredients_length(min=3, max=500)]
                                )
    preptime = IntegerField("Preparation time (minutes)",
                            [validators.required()]
                            )
    instruction = TextAreaField("Instruction",
                                [validators.Length(min=10, max=6000)]
                                )
    tags = TextAreaField("Tags", [validate_tag_length(min=3, max=18)])

    class Meta:
        csrf = False
