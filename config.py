import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 设置CSRF保护密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #  配置邮件服务器
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    # 默认本地服务器，无需验证
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    #  邮件端口号
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    # 本地端口号
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    #  启用传输层安全协议
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False')
    # 启用安全套接层协议
    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False')
    # 邮件账户的用户名
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'None')
    # 邮件账户的密码
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'None')
    # flask-mail主题前缀/发邮件人等配置
    FLASK_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASK_MAIL_SENDER = 'sishuiyibai@163.com'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    #  数据库配置
    # flask-sqlalchemy 2.0 版本以上被移除
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 分页显示设置
    FLASK_POSTS_PER_PAGE = 5
    FLASK_FOLLOWERS_PER_PAGE = 5
    FLASK_COMMENTS_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'
    # 测试配置中禁用 CSRF 保护
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig}







