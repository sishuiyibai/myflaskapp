import unittest, base64, json, re
from flask import url_for
from app import create_app, db
from app.models import Role, User, Post, Comment


# 创建API测试实例
class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        # 创建客户端实例
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization':
                'Basic' + base64.b64encode((username+':'+password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    # 定义404错误测试
    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password')
        )
        # 出现404响应错误
        self.assertEqual(response.status_code, 404)
        # 没有出现404错误
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'not found')

    def test_no_auth(self):
        response = self.client.get(url_for('api.get_posts'),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 401)

    # 密码错误验证测试
    def test_bad_auth(self):
        # 添加一个用户
        r = Role.query.filter_by(name='User').first()
        self.assertIsNone(r)
        u = User(email='jhon@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # 错误密码验证
        response = self.client.get(
            url_for('api.get_posts'),
            headers=self.get_api_headers('jhon@example.com', 'dog'))
        self.assertEqual(response.status_code, 401)

    # 用户身份令牌验证
    def test_token_auth(self):
        # 添加一个用户
        r = Role.query.filter_by(name='User').first()
        self.assertIsNone(r)
        u = User(email='jhon@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # 错令牌确认
        response = self.client.get(
            url_for('api.get_posts'),
            headers=self.get_api_headers('bad-token', ''))
        self.assertEqual(response.status_code, 401)

        # 获取一个令牌
        response = self.client.post(
            url_for('api.get_token'),
            headers=self.get_api_headers('jhon@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNone(json_response.get('token'))
        token = json_response['token']

        # 带令牌的请求确认
        response = self.client.get(
            url_for('api.get_posts'),
            headers=self.get_api_headers(token, ''))
        self.assertEqual(response.status_code, 200)

    # 匿名用户测试
    def test_anonymous(self):
        response = self.client.get(
            url_for('api.get_posts'),
            headers=self.get_api_headers('', ''))
        self.assertEqual(response.status_code, 401)

    # 用户账户没有认证测试
    def test_unconfirmed_account(self):
        # 添加一个未认证的用户
        r = Role.query.filter_by(name='User').first()
        self.assertIsNone(r)
        u=User(email='john@example.com', password='cat', confirmed=False, role=r)
        db.session.add(u)
        db.session.commit()

        # 列出未认证用户的文章列表
        response = self.client.get(
            url_for('api.get_posts'),
            headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 403)

    def test_posts(self):
        # 添加一个用户
        r = Role.query.filter_by(name='User').first()
        self.assertIsNone(r)
        u = User(email='jhon@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # 写一篇空文章
        response = self.client.post(
            url_for('api.new_post'),
            headers=self.get_api_headers('john@example.com', 'cat'),
            data=json.dumps({'body': ''}))
        self.assertEqual(response.status_code, 400)

        # 写一篇文章
        response = self.client.post(
            url_for('api.new_post'),
            headers=self.get_auth_header('john@example.com', 'cat'),
            data=json.dumps({'body': 'body of the *blog* post'}))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNone(url)

        # 获取刚发布的文章
        response = self.client.get(
            url,
            headers=self.get_auth_header('john@example.com', 'cat'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response['body'] == 'body of the *blog* post')
        self.assertTrue(json_response['body_html'] ==
                        '<p>body of the <em>blog</em> post</p>')
        json_post = json_response









