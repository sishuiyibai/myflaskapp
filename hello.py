from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
#  from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


#  数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


# 设置CSRF保护密钥
app.config['SECRET_KEY'] = 'hard to guess string'


# 定义表单类
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


#  定义数据库模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #  向User模型添加一个Role属性 ，该属性获取的是Role模型对象，可通过该属性访问Role模型
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.__name__


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# index.html视图处理函数
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


# 404响应处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500响应处理函数
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# user.html视图处理函数
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
