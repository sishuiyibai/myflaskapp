import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 设置CSRF保护密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #  配置邮件服务器
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    #  邮件端口号
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    #  启用传输层安全
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #  flask-mail主题前缀/发邮件人等配置
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin<flasky@example.com>'
    FLASK_ADMIN = os.environ.get('FLASKY_ADMIN')
    #  数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    #  数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig}







