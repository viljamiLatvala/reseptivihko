from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, validators, ValidationError

##Validators for checking tag length or ingredient line length
# doesn't exeed set maximum lengths
def tag_length(min=-1, max=-1):
    message = 'Each tag must be between %d and %d characters long.' % (min, max)
    def _tag_length(form, field):
        tags = field.data.split(',')
        for tag in tags:
            tag = tag.strip()
            if len(tag) < min or max != -1 and len(tag) > max:
                raise ValidationError(message)
                break
    return _tag_length

def ingredients_length(min=-1, max=-1):
    message = 'Each ingredient line must be between %d and %d characters long.' % (min, max)
    def _ingredients_length(form, field):
        ingredients = field.data.splitlines()
        for line in ingredients:
            line = line.strip()
            if len(line) < min or max != -1 and len(line) > max:
                raise ValidationError(message)
                break
    return _ingredients_length

##Form for creating a recipe
###Should validator maxes be inherited from models.py?
class RecipeForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3, max=144)])
    ingredients = TextAreaField("Ingredients", [ingredients_length(min = 3, max = 500)])
    preptime = IntegerField("Preparation time (minutes)", [validators.required()])
    instruction = TextAreaField("Instruction", [validators.Length(min=10, max=6000)])
    tags = TextAreaField("Tags", [tag_length(min=3, max=18)])

    class Meta:
        csrf = False