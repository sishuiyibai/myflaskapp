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
@app.cli.command()
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


if __name__ == '__main__':
    app.run()