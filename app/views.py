import os

from flask import request, render_template, url_for, redirect, flash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required

from . import app, db
from .models import Category, Movie, User
from .forms import CategoryForm, MovieForm, MovieUpdateForm, UserLoginForm, UserRegisterForm

STATIC_ROOT = os.path.join('app', 'static')


def index():
    title = 'Онлайн Кинотеатр'
    movies = Movie.query.all()
    return render_template('index.html', title=title, movies=movies)


@login_required
def admin_category_create():
    form = CategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_category = Category(
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(new_category)
            db.session.commit()
            flash('Категория успешно сохранена', 'Успешно!')
            return redirect(url_for('index'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При сохранении категории произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('admin/form.html', form=form)


@login_required
def admin_category_list():
    category_list = Category.query.all()
    return render_template('admin/category_list.html', category_list=category_list)


@login_required
def admin_category_update(category_id):
    category = Category.query.get(category_id)
    form = CategoryForm(obj=category)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(category)
            db.session.add(category)
            db.session.commit()
            flash('Категория успешно обновлена', 'Успешно!')
            return redirect(url_for('admin_category_list'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При обновлении категории произошла ошибка. {". ".join(text_list)}', 'Ошибка!')

    return render_template('admin/form.html', form=form)


@login_required
def admin_category_delete(category_id):
    category = Category.query.get(category_id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('admin_category_list'))
    return render_template('admin/category_delete.html', category=category)


@login_required
def admin_movie_create():
    form = MovieForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image = form.image.data
            video = form.video.data
            slug = form.slug.data
            file_path = os.path.join(STATIC_ROOT, 'movie_files', slug)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            image_path = os.path.join(file_path, secure_filename(image.filename))
            video_path = os.path.join(file_path, secure_filename(video.filename))
            image.save(image_path)
            video.save(video_path)
            new_movie = Movie(
                name=form.name.data,
                description=form.description.data,
                year=form.year.data,
                category_id=form.category_id.data,
                image=f'movie_files/{slug}/{secure_filename(image.filename)}',
                video=f'movie_files/{slug}/{secure_filename(video.filename)}'
            )
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print(form.errors)
    return render_template('admin/form.html', form=form)


def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    title = movie.name
    return render_template('movie_detail.html', movie=movie, title=title)


def movie_search():
    search_name = request.args.get('search')
    if search_name:
        movie_list = db.session.query(Movie).filter(Movie.name.like(f'%{search_name}%'))
    else:
        movie_list = Movie.query.all()
    return render_template('movie_search.html', movie_list=movie_list)


@login_required
def admin_movie_list():
    movie_list = Movie.query.all()
    return render_template('admin/movie_list.html', movie_list=movie_list)


@login_required
def admin_movie_update(movie_id):
    movie = Movie.query.get(movie_id)
    form = MovieUpdateForm(obj=movie)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(movie)
            db.session.add(movie)
            db.session.commit()
            return redirect(url_for('admin_movie_list'))
        else:
            print(form.errors)

    return render_template('admin/form.html', form=form)


@login_required
def admin_movie_delete(movie_id):
    movie = Movie.query.get(movie_id)
    if request.method == 'POST':
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('admin_movie_list'))
    return render_template('admin/movie_delete.html', movie=movie)


def user_register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегистрирован', 'Успех!')
            return redirect(url_for('user_login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации произошла ошибка. {". ".join(text_list)}', 'Ошибка!')
    return render_template('account/index.html', form=form, title=title)


def user_login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему', 'Успех!')
                return redirect(url_for('index'))
            else:
                flash('Невеные логин и пароль', 'Ошибка!')
    return render_template('account/index.html', form=form, title=title)


def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

