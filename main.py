from flask import request, make_response, redirect, render_template, url_for, session
from app import create_app
from app.forms import LoginForm
import unittest


app = create_app()
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

todos = ['ver el curso', 'revisar email', 'leer docs']

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response

@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'user_ip':user_ip, 
        'todos':todos,
        'username': username
    }

    return render_template('file.html', **context)

