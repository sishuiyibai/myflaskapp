#!/usr/bin/env python
import os
# coverage代码覆盖检测工具启动脚本配置
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import User, Role, Post, Permission, Comment, Follow
# from flask_script import Manager, Shell
from flask_migrate import Migrate
import click


# 工厂函数创建app实例，默认为config.py中的DevelopmentConfig配置,则使用data-dev.sqlite数据库
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#  向Flask插入外部脚本的Manager实例
# manager = Manager(app)
#  配置Flask-Migrate,创建数据库迁移仓库
migrate = Migrate(app, db)
# 导出数据库迁移命令
# manager.add_command('db', MigrateCommand)


# shell命令添加上下文
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,
                Post=Post, Permission=Permission, Comment=Comment, Follow=Follow)

# 注册shell 上下文
# manager.add_command("shell", Shell(make_context=make_shell_context))
#  启动单元测试的命令


# 使用Command实例的@option修饰符
@app.cli.command
@click.option('--coverage/--no-coverage', help='Run tests under coder coverage.', default=False)
def test(coverage):
    """Run the unit tests."""
    # 假如coverage设置为True并且环境参数FLASK_COVERAGE没有设置,则设置对应参数
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version:file://%s/index.html' % covdir)
        COV.erase()


# 添加部署命令
@app.cli.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # 把数据库迁移到最新修订版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()

    # 让所有用户都关注此用户
    User.add_self_follows()


# 在请求分析器的监视下运行程序
@app.cli.command
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profile data files are saved.')
def profile(length,profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import  ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],profile_dir=profile_dir)
    app.run(debug=False)


if __name__ == '__main__':
    app.run()