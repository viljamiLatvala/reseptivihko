from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, validators

class RecipeForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3)])
    ingredients = TextAreaField("ingredients", [validators.Length(min=10)])
    preptime = IntegerField("Preparation time (minutes)", [validators.required()])
    instruction = TextAreaField("Instruction", [validators.Length(min=10)])
    tags = TextAreaField("Tags")

    class Meta:
        csrf = False

class RecipeEditForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3)])
    ingredients = TextAreaField("ingredients", [validators.Length(min=10)])
    preptime = IntegerField("Preparation time (minutes)", [validators.required()])
    instruction = TextAreaField("Instruction", [validators.Length(min=10)])
    tags = TextAreaField("Tags")
 
    class Meta:
        csrf = False