from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager


#  bootstrap扩展框架
bootstrap = Bootstrap()

# 配置Mail
mail = Mail()

moment = Moment()

#  数据库引擎管理实例
db = SQLAlchemy()

login_manager = LoginManager()
# 启用会话保护[None,Basic,Strong]
login_manager.session_protection = 'strong'
# 设置登陆视图，用于未授权操作的跳转：
login_manager.login_view = 'auth.login'


# 工厂函数
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 注册main蓝本,main蓝本在./main文件夹下的__init__py文件中创建
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册auth蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    #  附加路由和自定义的错误页面

    return app