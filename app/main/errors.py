from flask import render_template, request, jsonify
from . import main


# 403： 禁止/响应处理函数,使用HTTP内容协商处理
@main.app_errorhandler(403)
def forbidden(e):
    # 请求内容格式为json格式，非html格式，则返回json格式的响应
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    # 请求内容格式为html格式，则返回html格式的响应
    return render_template('403.html'), 403


# 404： 未找到/响应处理函数,使用HTTP内容协商处理
@main.app_errorhandler(404)
def page_not_found(e):
    # 请求内容格式为json格式，非html格式，则返回json格式的响应
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    # 请求内容格式为html格式，则返回html格式的响应
    return render_template('404.html'), 404


# 500:  内部服务器错误/响应处理函数,使用HTTP内容协商处理
@main.app_errorhandler(500)
def internal_server_error(e):
    # 请求内容格式为json格式，非html格式，则返回json格式的响应
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    # 请求内容格式为html格式，则返回html格式的响应
    return render_template('500.html'), 500
