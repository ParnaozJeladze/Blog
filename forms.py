from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class AddBlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
    img = FileField("Choose your photo", validators=[FileAllowed(["jpeg", "jpg", "png","webp"])])
    submit = SubmitField("Post")


class RegisterForm(FlaskForm):
    username = StringField("Choose your username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=12,
                                                                            message="Your password must be at least "
                                                                                    "8 characters")])
    repeat_password = PasswordField("Repeat your password",
                                    validators=[DataRequired(),
                                                EqualTo("password", message="Your passwords must match"),
                                                Length(min=8, max=12)])

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

    submit = SubmitField("Login")


class ResetRequestForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Reset Password")


class EditBlogForm(FlaskForm):
    title = StringField("Title", )
    content = StringField("Content", )
    img = FileField("Choose your photo", validators=[FileAllowed(["jpeg", "jpg", "png","webp"])])
    submit = SubmitField("Post")
