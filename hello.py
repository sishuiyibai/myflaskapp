from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
#  from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


# 设置CSRF保护密钥
app.config['SECRET_KEY'] = 'hard to guess string'


# 定义表单类
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# index.html视图处理函数
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
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
