#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


# 工厂函数创建app实例，默认为config.py中的DevelopmentConfig配置,则使用data-dev.sqlite数据库
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#  向Flask插入外部脚本的Manager实例
manager = Manager(app)
#  配置Flask-Migrate,创建数据库迁移仓库
migrate = Migrate(app, db)
# 导出数据库迁移命令
manager.add_command('db', MigrateCommand)


# shell命令添加上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


# 注册shell 上下文
manager.add_command("shell", Shell(make_context=make_shell_context))
#  启动单元测试的命令


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()