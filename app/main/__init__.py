from flask import Blueprint
from ..models import Permission


#  创建蓝本
main = Blueprint('main', __name__)


# 使用上下文处理器，将Permission类在所有模版中全局可访问
@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)


from . import views, errors
