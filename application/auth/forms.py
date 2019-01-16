from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError


def validate_password(min=-1, max=-1):
    def _validate_password(form, field):
        password = field.data

        if len(password) < min or max != -1 and len(password) > max:
            raise ValidationError('Password must be between %d and %d'
                                  ' characters long.' % (min, max))
        if password == password.upper() or password == password.lower():
            raise ValidationError('Password must contain both upper'
                                  ' case and lower case letters.')
        has_numbers = False
        has_letters = False
        for char in password:
            if char.isdigit():
                has_numbers = True
            elif char.isalpha():
                has_letters = True

        if not has_numbers and has_letters:
            raise ValidationError('Password must contain'
                                  ' both letters and numbers.')

    return _validate_password


def validate_password_control(form, field):
    if not field.data == form.password.data:
        raise ValidationError("Passwords don't match!")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class SignupForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=16)])
    password = PasswordField("Password", [validate_password(min=8, max=144)])
    password_control = PasswordField("Re-type password",
                                     [validate_password_control])

    class Meta:
        csrf = False
