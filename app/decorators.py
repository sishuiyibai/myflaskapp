from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# 常规权限检查装饰器
def permission_required(permission):
    # 定义装饰器函数,用来修饰函数f（）（被修饰的函数）
    def decorator(f):
        # 调用包装器函数，保留原来f()函数的函数名及相关属性
        @wraps(f)
        # 修饰函数名
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            # 返回被修饰的函数
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 管理员权限装饰器
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
