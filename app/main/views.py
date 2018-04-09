from flask import render_template
from . import main


# index.html视图处理函数
@main.route('/')
def index():
    return render_template('index.html')


# user.html视图处理函数
@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
