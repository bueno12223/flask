from app.forms import LoginForm
from flask import render_template, redirect, session, flash, url_for
from . import auth
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel
@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)
        if user_doc.to_dict() is not None:
            password_db = user_doc.to_dict()['password']
            if check_password_hash(password_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)

                redirect(url_for('hello'))
            else:
                flash('Usuario o contraseña incorrectas')
        else:
            flash('Usario no existe')
        session['username'] = username
        return redirect(url_for('index'))
        
    return render_template('login.html', **context)

@auth.route('/logut')
@login_required
def logout():
    logout_user()
    return redirect('login')


@auth.route('/singup', methods=['GET', 'POST'])
def singup():
    singup_form = LoginForm()
    context = {
        'singup_form': singup_form
    }
    if singup_form.validate_on_submit():
        username = singup_form.username.data
        password = singup_form.password.data
        user_doc = get_user(username).to_dict()
        if user_doc is None:
            password = generate_password_hash(password)
            user_data = UserData(username, password)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Usuario registrado exitosamente')
            return redirect(url_for('hello'))
        else:
            flash('Usario ya registrado')
    return render_template('singup.html', **context)