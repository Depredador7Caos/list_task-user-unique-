from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from content.models import *
from content import db

authentication = Blueprint("authentication", __name__, url_prefix="/auth")


@authentication.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # objeto
        usuario = User(username, generate_password_hash(password))

        error = None

        user_name = User.query.filter_by(username = username).first()

        #Comparara si el username existe o no
        if user_name == None:
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('authentication.logeo'))
        else:
            error = f"El usuario {username} Ya esta disponible."

        flash(error)
    return render_template('auth/register.html')

@authentication.route('/logeo', methods=['GET', 'POST'])
def logeo():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        # VALIDAR DATOS
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user_name.password, password):
            error = 'Contraseña incorrecta'

        # INICIAR SESSION
        if error == None:
            session.clear()
            session['user_id'] = user_name.id
            return redirect(url_for('frontPage.lista'))
        flash(error)
    return render_template('auth/login.html')

# funciona para mantener una session iniciada, y sbaer si esta iniciado y cuando no
@authentication.before_app_request
def load_logged_in_user():
    user_name_id = session.get('user_id')

    if user_name_id is None:
        g.user_name = None
    else:
        g.user_name = User.query.get_or_404(user_name_id)

# FUNCION PARA CERRR SESSION
@authentication.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user_name is None:
            return redirect(url_for('authentication.logeo'))
        return view(**kwargs)
    return wrapped_view
