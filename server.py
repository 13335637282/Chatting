import logging
import sqlite3
import hashlib
import uuid

from flask import Flask, request, jsonify, url_for

app = Flask(__name__)

token_map:dict = {}
api_version = "v1"

logger = logging.getLogger("server/root")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s/%(name)s %(levelname)s]%(filename)s.%(funcName)s(%(lineno)s):\n %(message)s')
logger.addHandler(logging.FileHandler('server.log'))

# ---------- 初始化数据库 ----------
def init_db():
    conn = sqlite3.connect('login.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- 数据库连接辅助 ----------
def get_db():
    conn = sqlite3.connect('login.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- 哈希工具 ----------
def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

# ========== RESTful 资源端点 ==========

# ----- 资源：用户 (User) -----
@app.route(f'/api/{api_version}/users', methods=['POST'])
def create_user():
    """
    创建新用户（注册）
    ---
    POST /api/v1/users
    {
        "username": "alice",
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体必须为JSON'}), 400

    username = data.get('username')
    password_hash = data.get('password_hash')

    if not username or not password_hash:
        return jsonify({'error': '用户名和密码哈希不能为空'}), 400

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': '用户名已存在'}), 409
    conn.close()

    # 返回 201 Created，并附带新用户资源位置（可选）
    response = jsonify({
        'message': '用户创建成功'
    })
    response.status_code = 201
    response.headers['Location'] = url_for('get_user', username=username, _external=True)
    return response

@app.route(f'/api/{api_version}/users/<token>', methods=['GET'])
def get_user(token:str):
    """
    获取用户信息（演示资源定位，仅返回基本信息）
    ---
    GET /api/v1/users/alice
    """
    if (token_map.get(token) is None):
        return jsonify({'error': 'token 错误'}), 401 #TODO 错误码
    else:
        username = token_map.get(token)
    conn = get_db()
    user = conn.execute(
        'SELECT id, username FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': '用户不存在'}), 404

def random_token() -> str:
    for i in range(10):
        token = str(uuid.uuid4())
        if token_map.get(token) is None:
            return str(token)
    return ""

# ----- 资源：会话 (Session) -----
@app.route(f'/api/{api_version}/sessions', methods=['POST'])
def create_session():
    """
    创建会话（登录）
    ---
    POST /api/v1/sessions
    {
        "username": "alice",
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    }
    成功时返回 200 和简单消息（实际生产应返回 token）
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体必须为JSON'}), 400

    username = data.get('username')
    password_hash = data.get('password_hash')

    if not username or not password_hash:
        return jsonify({'error': '用户名和密码哈希不能为空'}), 400

    conn = get_db()
    user = conn.execute(
        'SELECT password_hash FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()

    if user and user['password_hash'] == password_hash:
        token = random_token()
        token_map[token] = username
        logger.debug(f"token_map: {str(token_map)}")
        # 登录成功，可在此生成 JWT 或 Session Token，示例中只返回消息
        return jsonify({
            'message': '登录成功',
            'username': username,
            'token': token
        }), 200
    else:
        return jsonify({'error': '用户名或密码错误'}), 401

@app.route(f'/api/{api_version}/sessions', methods=['DELETE'])
def delete_session():
    if token_map.get(request.get_json().get('token')) is None:
        return jsonify({"error":"token 失效"}), 401
    else:
        data = request.get_json()
        if not data:
            return jsonify({"error":"请求体不是JSON"}), 400
        token = data.get('token')
        token_map.pop(token)

    return jsonify({"msg":"完成"}), 200


# ---------- 健康检查（可选） ----------
@app.route(f'/api/{api_version}/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)