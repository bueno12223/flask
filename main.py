from flask import request, make_response, redirect, render_template, url_for, session
from app import create_app
from app.forms import LoginForm, TodoForm, DeleteForm, UpdateTodoForm
from flask_login import login_required, current_user
from app.firestore_service import get_users, get_todos, put_todo, update_todo, delete_todo
import unittest


app = create_app()
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteForm()
    update_form = UpdateTodoForm()
    print(get_todos(username))
    context = {
        'user_ip': user_ip,
        'todos': get_todos(username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form
    }
    if todo_form.validate_on_submit():
        description = todo_form.description.data
        put_todo(username, description)
        return redirect(url_for('hello'))
    users = get_users()

    return render_template('file.html', **context)

@app.route('/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))

@app.route('/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for('hello'))