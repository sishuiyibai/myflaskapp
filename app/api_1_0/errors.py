from flask import jsonify
from app.exceptions import ValidationError
from . import api


# API 蓝本中 400 状态码的错误处理程序
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


# API 蓝本中 401 状态码的错误处理程序
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message':message})
    response.status_code = 401
    return response


# API 蓝本中 403 状态码的错误处理程序
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


# 定义全局的API异常的处理程序
@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])