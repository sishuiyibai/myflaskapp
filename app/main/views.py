from flask import render_template, abort, flash, redirect, url_for
from app import db
from . import main
from .forms import EditProfileForm
from ..models import User
from flask_login import login_required, current_user


# index.html视图处理函数
@main.route('/')
def index():
    return render_template('index.html')


# user.html视图处理函数
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


# 普通用户编辑资料路由
@main.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        # 对象添加到数据库会话中
        db.session.add(current_user)
        # 会话内容保存到数据库中
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


