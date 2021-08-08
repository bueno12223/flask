from flask import Flask, request, make_response, redirect, render_template
app = Flask(__name__)

todos = ['ver el curso', 'revisar email', 'leer docs']

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('ip', user_ip)
    return response

@app.route('/hello')
def hello():
    user_ip = request.cookies.get('ip')
    context = {
        'user_ip':user_ip, 
        'todos':todos
    }
    return render_template('file.html', **context)