from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .forms import *
from .utils import *

main = Blueprint('main',__name__)

@main.route('/', methods = ['GET','POST'])
def index():
    """
    The Major route, here the user can convert videos into mp3 or wav, 
    and download on his own machine
    """
    username = request.cookies.get('username')
    form = LinkForm()

    if form.validate_on_submit():
        link = form.yt_link.data
        audio_format = request.form.get('audioFormat')
        user = Users.get(Users.username == username)

        download_yt_audio(link, "./files", audio_format)
        author, title =  get_video_info(link)

        audio = Audios(title = title, author = author, path = "./files",user_id = user.id)


    return render_template("index.html",username = username, form = form)

@main.route('/collections', methods = ['GET'])
def collections():
    username = request.cookies.get('username')
    return render_template("collections.html", username = username)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = Users.get_or_none(Users.username == form.username.data)
        if existing_user:
            flash('Username Already exists.', 'danger')
            return render_template('register.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data)
        user = Users.create(username=form.username.data, password=hashed_password)
        flash('Created Account, now you can make the login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_or_none(Users.username == form.username.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)

            response = redirect(url_for('main.index'))
            response.set_cookie('username', form.username.data, httponly=True, 
                secure=False, 
                samesite='Lax', 
                path='/', 
                max_age=30*24*60*60
            )
            
            return response
        else:
            flash('User or password incorrect.', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    response = redirect(url_for('main.index'))
    response.set_cookie('username', '', expires=0)
    return response