from flask import Blueprint, render_template, request, redirect, url_for, session, g
from content.auth import login_required
from content.models import *
from content import db

frontPage = Blueprint("frontPage", __name__, url_prefix="/todo")

#-------------------RUTA LISTA DE TAREAS----------------------
@frontPage.route('/lista')
@login_required
def lista():
    tareas = Task.query.all()
    return render_template('todo/index.html', tareas = tareas)

#-------------------RUTA CREAR NUEVA TAREA--------------------
@frontPage.route('/create', methods=['GET', 'POST'])
@login_required
def create_new_task():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        tarea = Task(g.user_name.id, title, desc)

        db.session.add(tarea)
        db.session.commit()

        return redirect(url_for('frontPage.lista'))
    return render_template('todo/create.html')


# FUNCION QUE MANDA ID HACIA LAS RUTAS UPDATE Y DELETE
def get_tarea(id):
    tarea = Task.query.get_or_404(id)
    return tarea

#-------------------RUTA ACTUALIZAR TAREA--------------------
@frontPage.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):

    tarea = get_tarea(id)

    if request.method == 'POST':
        tarea.title = request.form['title']
        tarea.desc = request.form['desc']
        tarea.state = True if request.form.get('state') == 'on' else False

        db.session.commit()
        return redirect(url_for('frontPage.lista'))
    return render_template('todo/update.html', tarea = tarea)

#------------------RUTA ELIMINAR TAREA-----------------------
@frontPage.route('/delete/<int:id>')
@login_required
def delete_task(id):

    tarea = get_tarea(id)
    db.session.delete(tarea)
    db.session.commit()

    return redirect(url_for('frontPage.lista'))
