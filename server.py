import base64
import logging
import os
import sqlite3
import uuid
from pathlib import Path

from argon2 import PasswordHasher
import rsa
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from flask import Flask, request, jsonify, url_for
from rsa import PrivateKey

from client import debug_print

__license__ = """Apache License 2.0"""

app = Flask(__name__)

token_map:dict = {}
api_version = "v1"
ph = PasswordHasher()

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
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def create_rsa_key():
    logger.info("正在检测是否有公私钥中...")
    if not os.path.exists("PUBLIC_KEY.chatting") and not os.path.exists("PRIVATE_KEY.chatting"):
        logger.info("未检测到有公钥和私钥，正在自动生成。")
        public_key, private_key = rsa.newkeys(2048 * 2)
        with open("PUBLIC_KEY.chatting", 'wb') as f:
            f.write(public_key.save_pkcs1())
            f.close()
        with open("PRIVATE_KEY.chatting", 'wb') as f:
            f.write(private_key.save_pkcs1())
            f.close()

        logger.info("生成完成。")
        return
    logger.info("检测到公私钥 √")

def rsa_decrypt(bytes_:bytes):
    with open("PRIVATE_KEY.chatting", mode='rb') as fread:
        priv_key = PrivateKey.load_pkcs1(fread.read())
        fread.close()

    cipher_bin = rsa.decrypt(bytes_, priv_key)
    return cipher_bin

# ---------- 数据库连接辅助 ----------
def get_db():
    conn = sqlite3.connect('login.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- 哈希工具 ----------
def hash(text: str) -> str:
    return ph.hash(text)

# ========== RESTful 资源端点 ==========

# ----- 资源：用户 (User) -----
@app.route(f'/api/{api_version}/users', methods=['POST'])
def create_user():
    """
    创建新用户（注册）
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体必须为JSON'}), 400

    try:
        username = data.get('username')
        password = rsa_decrypt(base64.b64decode(data.get('password'))).decode()
    except:
        return jsonify({"error": "服务器无法理解客户端的请求"}), 400

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    password = ph.hash(password).replace(" ","")
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': '用户名已存在'}), 409
    conn.close()

    return jsonify({'message':"用户创建成功"}), 201

@app.route(f'/api/{api_version}/users/<token>', methods=['GET'])
def get_user(token:str):
    """
    获取用户信息（演示资源定位，仅返回基本信息）
    ---
    GET /api/v1/users/alice
    """
    if (token_map.get(token) is None):
        return jsonify({'error': 'token 错误'}), 401
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
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体必须为JSON'}), 400

    try:
        username = data.get('username')
        password = rsa_decrypt(base64.b64decode(data.get('password'))).decode()
    except:
        logger.error("服务器解析")
        return jsonify({"error":"服务器无法理解客户端的请求，请确认客户端版本正确。"}), 400

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400


    conn = get_db()
    user = conn.execute(
        'SELECT password FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()

    if user:
        try:
            is_valid = ph.verify(user['password'], password)
            if not is_valid:
                raise VerificationError
        except VerifyMismatchError :
            return jsonify({'error': '用户名或密码错误'}), 401
        except VerificationError:
            return jsonify({'error': '用户名或密码错误'}), 401
        except InvalidHashError:
            return jsonify({'error': '不合法的Hash'}), 401

        token = random_token()
        token_map[token] = username
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
    create_rsa_key()
    app.run(host='127.0.0.1', port=5000, debug=True)