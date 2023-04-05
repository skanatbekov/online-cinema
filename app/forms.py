from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
import wtforms as wf
from werkzeug.utils import secure_filename


from .models import User
from . import app
from .models import Category


def category_choices():
    choices = []
    with app.app_context():
        categories = Category.query.all()
        for category in categories:
            choices.append((category.id, category.name))
    return choices


class CategoryForm(FlaskForm):
    name = wf.StringField(label="Название категории", validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=60)
    ])
    description = wf.TextAreaField(label="Описание категории", validators=[
        wf.validators.Length(min=3, max=255)
    ])

    def validate_name(self, field):
        words = field.data.split(' ')
        for word in words:
            if not word.isalpha():
                raise wf.ValidationError('В названии не должно быть символов')


class MovieForm(FlaskForm):
    slug = wf.StringField(label="Идентификатор фильма")
    name = wf.StringField(label="Название фильма", validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=60)
    ])
    description = wf.TextAreaField(label="Описание фильма", validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=255)
    ])
    year = wf.IntegerField(label="Год выпуска")
    category_id = wf.SelectField(label="Жанр фильма", choices=category_choices)
    image = FileField(label="Главная картинка", validators=[FileRequired(), ])
    video = FileField(label="Видеофайл", validators=[FileRequired(), ])


class MovieUpdateForm(FlaskForm):
    name = wf.StringField(label="Название фильма", validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=60)
    ])
    description = wf.TextAreaField(label="Описание фильма", validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=255)
    ])
    year = wf.IntegerField(label="Год выпуска")
    category_id = wf.SelectField(label="Жанр фильма", choices=category_choices)


class UserLoginForm(FlaskForm):
    username = wf.StringField(label='Логин', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=20)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate_password(self, field):
        if len(field.data) < 8:
            raise wf.ValidationError('Длина пароля должна быть минимум 8 символов')


class UserRegisterForm(UserLoginForm):
    password_2 = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate(self, *args, **kwargs):
        if not super().validate(*args, **kwargs):
            return False
        if self.password.data != self.password_2.data:
            self.password_2.errors.append('Пароли должны совпадать')
            return False
        return True

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise wf.ValidationError('Пользователь с таким логином уже существует')