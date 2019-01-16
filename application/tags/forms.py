from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, HiddenField, validators, ValidationError

class TagForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3, max=144)])
    description = TextAreaField("Description", [validators.Length(max=144)])

    class Meta:
        csrf = False