import base64
import hashlib
import json
import logging
import os
import secrets
import sqlite3
import uuid
from datetime import datetime

import rsa
from argon2 import PasswordHasher
from argon2.exceptions import (InvalidHashError, VerificationError,
                               VerifyMismatchError)
from flask import Flask, jsonify, request
from rsa import PrivateKey

__license__ = """Apache License 2.0"""

app = Flask(__name__)

token_map: dict = {}  # token -> username
api_version = "v1"
ph = PasswordHasher()

logger = logging.getLogger("server/root")
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s/%(name)s %(levelname)s]%(filename)s.%(funcName)s(%(lineno)s):\n %(message)s",
)
logger.addHandler(logging.FileHandler("server.log"))


# ---------- 初始化数据库 ----------
def init_login_db() -> None:
    """初始化一个 login.db 数据库，使用sqlite库创建"""
    conn = sqlite3.connect("login.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def init_friend_db() -> None:
    """初始化 friends.db 数据库，使用sqlite库创建"""
    conn = sqlite3.connect("friends.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            friend_username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, friend_username)
        )
    """)
    conn.commit()
    conn.close()


def init_friend_requests_db() -> None:
    """初始化好友请求数据库"""
    conn = sqlite3.connect("friend_requests.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS friend_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_username TEXT NOT NULL,
            to_username TEXT NOT NULL,
            status TEXT DEFAULT 'pending',  -- pending, accepted, rejected
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(from_username, to_username)
        )
    """)
    conn.commit()
    conn.close()


def init_user_profile_db() -> None:
    """初始化用户资料数据库"""
    conn = sqlite3.connect("user_profile.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            username TEXT PRIMARY KEY,
            nickname TEXT,
            birthday TEXT,
            gender TEXT,
            avatar TEXT,
            email TEXT,
            phone TEXT,
            bio TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


init_friend_db()
init_login_db()
init_friend_requests_db()
init_user_profile_db()


def create_rsa_key() -> None:
    """
    如果 RSA 公私钥不存在 则自动生成
    """
    logger.info("正在检测是否有公私钥中...")
    if not os.path.exists("PUBLIC_KEY.chatting") and not os.path.exists(
            "PRIVATE_KEY.chatting"
    ):
        logger.info("未检测到有公钥和私钥，正在自动生成。")
        public_key, private_key = rsa.newkeys(2048 * 2)
        with open("PUBLIC_KEY.chatting", "wb") as f:
            f.write(public_key.save_pkcs1())
        with open("PRIVATE_KEY.chatting", "wb") as f:
            f.write(private_key.save_pkcs1())
        logger.info("生成完成。")
        return
    logger.info("检测到公私钥 √")


def rsa_decrypt(bytes_: bytes) -> bytes:
    with open("PRIVATE_KEY.chatting", "rb") as fread:
        priv_key = PrivateKey.load_pkcs1(fread.read())
    cipher_bin = rsa.decrypt(bytes_, priv_key)
    return cipher_bin


# ---------- 数据库连接辅助 ----------
def get_login_db() -> sqlite3.Connection:
    """
    获取login.db的sqlite3 Connection 对象
    """
    conn = sqlite3.connect("login.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_friend_db() -> sqlite3.Connection:
    """
    获取friends.db的sqlite3 Connection 对象
    """
    conn = sqlite3.connect("friends.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_friend_requests_db() -> sqlite3.Connection:
    """
    获取friend_requests.db的sqlite3 Connection 对象
    """
    conn = sqlite3.connect("friend_requests.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_user_profile_db() -> sqlite3.Connection:
    """
    获取user_profile.db的sqlite3 Connection 对象
    """
    conn = sqlite3.connect("user_profile.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- 辅助函数 ----------
def verify_token(token: str) -> tuple:
    """
    验证token并返回用户名
    返回: (is_valid, username)
    """
    if token_map.get(token) is None:
        return False, None

    username = token_map.get(token)
    conn = get_login_db()
    user = conn.execute(
        "SELECT username FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user:
        return True, username
    else:
        return False, None


def are_friends(username1: str, username2: str) -> bool:
    """检查两个用户是否为好友"""
    conn = get_friend_db()
    friend = conn.execute(
        "SELECT id FROM friends WHERE username = ? AND friend_username = ?",
        (username1, username2),
    ).fetchone()
    conn.close()
    return friend is not None


@app.route(f"/api/{api_version}/users", methods=["POST"])
def create_user():
    """
    创建新用户（api POST /users）
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体必须为JSON"}), 400

    try:
        username = data.get("username")
        password = rsa_decrypt(base64.b64decode(data.get("password"))).decode()
    except Exception:
        return jsonify({"error": "服务器无法理解客户端的请求"}), 400

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    password = ph.hash(password).replace(" ", "")
    conn = get_login_db()
    try:
        # 插入用户
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()

        # 创建用户资料
        profile_conn = get_user_profile_db()
        profile_conn.execute(
            "INSERT INTO user_profiles (username) VALUES (?)",
            (username,),
        )
        profile_conn.commit()
        profile_conn.close()

    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "用户名已存在"}), 409
    conn.close()

    return jsonify({"message": "用户创建成功"}), 201


@app.route(f"/api/{api_version}/users/<username>", methods=["GET"])
def get_user(username: str):
    """
    获取用户信息（仅对好友开放）
    """
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, current_user = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 检查是否是自己
    if current_user == username:
        # 可以查看自己的信息
        conn = get_login_db()
        user = conn.execute(
            "SELECT username, created_at FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "用户不存在"}), 404

        # 获取用户资料
        profile_conn = get_user_profile_db()
        profile = profile_conn.execute(
            "SELECT * FROM user_profiles WHERE username = ?", (username,)
        ).fetchone()
        profile_conn.close()

        result = dict(user)
        if profile:
            # 移除username避免重复
            profile_dict = dict(profile)
            profile_dict.pop('username', None)
            result.update(profile_dict)

        return jsonify(result), 200
    else:
        # 检查是否为好友
        if are_friends(current_user, username):
            conn = get_login_db()
            user = conn.execute(
                "SELECT username, created_at FROM users WHERE username = ?", (username,)
            ).fetchone()
            conn.close()

            if not user:
                return jsonify({"error": "用户不存在"}), 404

            # 获取用户资料
            profile_conn = get_user_profile_db()
            profile = profile_conn.execute(
                "SELECT * FROM user_profiles WHERE username = ?", (username,)
            ).fetchone()
            profile_conn.close()

            result = dict(user)
            if profile:
                # 移除username避免重复
                profile_dict = dict(profile)
                profile_dict.pop('username', None)
                result.update(profile_dict)

            return jsonify(result), 200
        else:
            return jsonify({"error": "只有好友才能查看详细信息"}), 403


@app.route(f"/api/{api_version}/users/<username>/profile", methods=["PUT"])
def update_user_profile(username: str):
    """
    更新用户资料
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体必须为JSON"}), 400

    token = data.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, current_user = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 只能更新自己的资料
    if current_user != username:
        return jsonify({"error": "只能更新自己的资料"}), 403

    # 可更新的字段
    allowed_fields = ['nickname', 'birthday', 'gender', 'avatar', 'email', 'phone', 'bio']
    update_data = {}
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]

    if not update_data:
        return jsonify({"error": "没有提供要更新的字段"}), 400

    # 构建更新语句
    set_clause = ", ".join([f"{field} = ?" for field in update_data.keys()])
    set_clause += ", updated_at = CURRENT_TIMESTAMP"
    values = list(update_data.values())
    values.append(username)

    conn = get_user_profile_db()
    conn.execute(
        f"UPDATE user_profiles SET {set_clause} WHERE username = ?",
        values
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "资料更新成功"}), 200


@app.route(f"/api/{api_version}/users/<old_username>/rename", methods=["PUT"])
def rename_user(old_username: str):
    """
    修改用户名
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体必须为JSON"}), 400

    token = data.get("token")
    new_username = data.get("new_username")

    if not token or not new_username:
        return jsonify({"error": "缺少token或新用户名"}), 400

    is_valid, current_user = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 只能修改自己的用户名
    if current_user != old_username:
        return jsonify({"error": "只能修改自己的用户名"}), 403

    # 验证新用户名格式
    if not new_username or len(new_username) < 3:
        return jsonify({"error": "用户名至少需要3个字符"}), 400

    # 开始事务处理（需要更新多个数据库）
    conn_login = get_login_db()
    conn_friend = get_friend_db()
    conn_requests = get_friend_requests_db()
    conn_profile = get_user_profile_db()

    try:
        # 检查新用户名是否已存在
        existing = conn_login.execute(
            "SELECT username FROM users WHERE username = ?", (new_username,)
        ).fetchone()
        if existing:
            return jsonify({"error": "用户名已存在"}), 409

        # 开始事务
        conn_login.execute("BEGIN TRANSACTION")
        conn_friend.execute("BEGIN TRANSACTION")
        conn_requests.execute("BEGIN TRANSACTION")
        conn_profile.execute("BEGIN TRANSACTION")

        # 更新login.db
        conn_login.execute(
            "UPDATE users SET username = ? WHERE username = ?",
            (new_username, old_username)
        )

        # 更新user_profile.db
        conn_profile.execute(
            "UPDATE user_profiles SET username = ? WHERE username = ?",
            (new_username, old_username)
        )

        # 更新friends.db (作为用户)
        conn_friend.execute(
            "UPDATE friends SET username = ? WHERE username = ?",
            (new_username, old_username)
        )
        # 更新friends.db (作为好友)
        conn_friend.execute(
            "UPDATE friends SET friend_username = ? WHERE friend_username = ?",
            (new_username, old_username)
        )

        # 更新friend_requests.db (作为发送者)
        conn_requests.execute(
            "UPDATE friend_requests SET from_username = ? WHERE from_username = ?",
            (new_username, old_username)
        )
        # 更新friend_requests.db (作为接收者)
        conn_requests.execute(
            "UPDATE friend_requests SET to_username = ? WHERE to_username = ?",
            (new_username, old_username)
        )

        # 更新token_map
        for token, username in list(token_map.items()):
            if username == old_username:
                token_map[token] = new_username

        # 提交所有事务
        conn_login.commit()
        conn_friend.commit()
        conn_requests.commit()
        conn_profile.commit()

    except Exception as e:
        # 回滚所有事务
        conn_login.rollback()
        conn_friend.rollback()
        conn_requests.rollback()
        conn_profile.rollback()
        logger.error(f"修改用户名失败: {str(e)}")
        return jsonify({"error": "修改用户名失败"}), 500
    finally:
        conn_login.close()
        conn_friend.close()
        conn_requests.close()
        conn_profile.close()

    return jsonify({
        "message": "用户名修改成功",
        "new_username": new_username
    }), 200


@app.route(f"/api/{api_version}/users/search", methods=["GET"])
def search_users():
    """
    搜索用户，返回用户名列表
    """
    query = request.args.get("q", "")
    token = request.args.get("token")

    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, current_user = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    if not query or len(query) < 2:
        return jsonify({"error": "搜索关键词至少需要2个字符"}), 400

    conn = get_login_db()
    # 搜索包含查询词的用户名，排除自己
    users = conn.execute(
        "SELECT username FROM users WHERE username LIKE ? AND username != ? LIMIT 50",
        (f"%{query}%", current_user)
    ).fetchall()
    conn.close()

    result = [user["username"] for user in users]
    return jsonify({"users": result}), 200


def random_token(length: int = 1024, iterations: int = 100000) -> str:
    """
    生成一个长度较长、计算速度较慢的随机Token。

    :param length:  Token的字符长度（必须为偶数，若为奇数则自动加1）
    :param iterations: PBKDF2迭代次数，控制计算耗时，默认为100000
    :return: 十六进制字符串表示的Token
    """
    key:bytes = b""
    while key.hex() in list(token_map.keys()) or key == b"":
        # 确保长度为偶数（十六进制编码需要）
        if length % 2 != 0:
            length += 1

        # 计算需要的字节数（十六进制每字符对应4比特，即2字符=1字节）
        byte_len = length // 2

        # 生成随机盐和密码（种子）
        salt = secrets.token_bytes(16)          # 16字节盐
        password = secrets.token_bytes(32)       # 32字节密码材料

        # 使用PBKDF2生成指定长度的密钥
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password,
            salt,
            iterations,
            dklen=byte_len
        )

    # 返回十六进制编码的Token
    return key.hex()


# ----- 资源：会话 (Session) -----
@app.route(f"/api/{api_version}/sessions", methods=["POST"])
def create_session():
    """
    api 接口 POST /sessions
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体必须为JSON"}), 400

    try:
        username = data.get("username")
        password = rsa_decrypt(base64.b64decode(data.get("password"))).decode()
    except Exception:
        logger.error("服务器解析")
        return (
            jsonify({"error": "服务器无法理解客户端的请求，请确认客户端版本正确。"}),
            400,
        )

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    conn = get_login_db()
    user = conn.execute(
        "SELECT password FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user:
        try:
            is_valid = ph.verify(user["password"], password)
            if not is_valid:
                raise VerificationError
        except VerifyMismatchError:
            return jsonify({"error": "用户名或密码错误"}), 401
        except VerificationError:
            return jsonify({"error": "用户名或密码错误"}), 401
        except InvalidHashError:
            return jsonify({"error": "不合法的Hash"}), 401

        token = random_token()
        for i in list(token_map.keys()):
            if token_map[i] == username:
                token_map.pop(i)
        token_map[token] = username
        logger.debug(f"{token_map[token]}")
        # 登录成功，返回 Token。
        return (
            jsonify({"message": "登录成功", "username": username, "token": token}),
            200,
        )
    else:
        return jsonify({"error": "用户名或密码错误"}), 401


@app.route(f"/api/{api_version}/friends/requests", methods=["POST"])
def send_friend_request():
    """
    发送好友请求
    API POST /friends/requests
    请求体: {
        "token": "用户token",
        "friend_username": "好友用户名",
        "message": "附加消息（可选）"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不是JSON"}), 400

    token = data.get("token")
    friend_username = data.get("friend_username")
    message = data.get("message", "")

    if not token or not friend_username:
        return jsonify({"error": "token和好友用户名不能为空"}), 400

    # 验证token
    is_valid, username = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 验证好友用户是否存在
    conn_login = get_login_db()
    friend_exists = conn_login.execute(
        "SELECT username FROM users WHERE username = ?", (friend_username,)
    ).fetchone()
    conn_login.close()

    if not friend_exists:
        return jsonify({"error": "好友用户不存在"}), 404

    # 不能添加自己为好友
    if username == friend_username:
        return jsonify({"error": "不能添加自己为好友"}), 400

    # 检查是否已经是好友
    conn = get_friend_db()
    existing_friend = conn.execute(
        "SELECT id FROM friends WHERE username = ? AND friend_username = ?",
        (username, friend_username),
    ).fetchone()
    if existing_friend:
        conn.close()
        return jsonify({"error": "已经是好友关系"}), 409

    # 检查是否已经存在好友请求
    conn_requests = get_friend_requests_db()
    existing_request = conn_requests.execute(
        """SELECT id, status FROM friend_requests 
           WHERE from_username = ? AND to_username = ?""",
        (username, friend_username),
    ).fetchone()

    if existing_request:
        if existing_request["status"] == "pending":
            conn_requests.close()
            return jsonify({"error": "已发送过好友请求，请等待对方处理"}), 409
        elif existing_request["status"] == "rejected":
            # 如果之前被拒绝，可以重新发送
            conn_requests.execute(
                """UPDATE friend_requests 
                   SET status = 'pending', message = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (message, existing_request["id"]),
            )
            conn_requests.commit()
            conn_requests.close()
            return jsonify({"message": "好友请求已重新发送"}), 200

    # 创建新的好友请求
    try:
        conn_requests.execute(
            """INSERT INTO friend_requests (from_username, to_username, message)
               VALUES (?, ?, ?)""",
            (username, friend_username, message),
        )
        conn_requests.commit()
    except sqlite3.IntegrityError:
        conn_requests.close()
        return jsonify({"error": "好友请求已存在"}), 409

    conn_requests.close()
    return jsonify({"message": "好友请求已发送"}), 201


@app.route(f"/api/{api_version}/friends/requests/incoming", methods=["GET"])
def get_incoming_requests():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, username = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 从 friend_requests.db 获取待处理的请求列表
    conn_req = get_friend_requests_db()
    requests = conn_req.execute(
        """SELECT id, from_username, message, status, created_at
           FROM friend_requests
           WHERE to_username = ? AND status = 'pending'
           ORDER BY created_at DESC""",
        (username,),
    ).fetchall()
    conn_req.close()

    result = []
    for req in requests:
        result.append(
            {
                "request_id": req["id"],
                "from_username": req["from_username"],
                "message": req["message"],
                "created_at": req["created_at"],
            }
        )

    return jsonify({"requests": result}), 200


@app.route(f"/api/{api_version}/friends/requests/outgoing", methods=["GET"])
def get_outgoing_requests():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, username = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 从 friend_requests.db 获取发出的请求列表
    conn_req = get_friend_requests_db()
    requests = conn_req.execute(
        """SELECT id, to_username, message, status, created_at
           FROM friend_requests
           WHERE from_username = ?
           ORDER BY created_at DESC""",
        (username,),
    ).fetchall()
    conn_req.close()

    result = []
    for req in requests:
        result.append(
            {
                "request_id": req["id"],
                "to_username": req["to_username"],
                "message": req["message"],
                "status": req["status"],
                "created_at": req["created_at"],
            }
        )

    return jsonify({"requests": result}), 200


@app.route(
    f"/api/{api_version}/friends/requests/<int:request_id>/accept", methods=["POST"]
)
def accept_friend_request(request_id):
    """
    接受好友请求
    API POST /friends/requests/<request_id>/accept
    请求体: {
        "token": "用户token"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不是JSON"}), 400

    token = data.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, username = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 获取好友请求信息
    conn_requests = get_friend_requests_db()
    friend_request = conn_requests.execute(
        "SELECT * FROM friend_requests WHERE id = ? AND status = 'pending'",
        (request_id,),
    ).fetchone()

    if not friend_request:
        conn_requests.close()
        return jsonify({"error": "好友请求不存在或已被处理"}), 404

    # 验证当前用户是请求的接收者
    if friend_request["to_username"] != username:
        conn_requests.close()
        return jsonify({"error": "无权操作此好友请求"}), 403

    from_username = friend_request["from_username"]

    # 开始事务处理
    try:
        # 更新请求状态
        conn_requests.execute(
            """UPDATE friend_requests 
               SET status = 'accepted', updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (request_id,),
        )
        conn_requests.commit()

        # 添加好友关系到friends表（双向）
        conn_friends = get_friend_db()

        # 添加 A -> B 的关系
        conn_friends.execute(
            "INSERT OR IGNORE INTO friends (username, friend_username) VALUES (?, ?)",
            (username, from_username),
        )

        # 添加 B -> A 的关系
        conn_friends.execute(
            "INSERT OR IGNORE INTO friends (username, friend_username) VALUES (?, ?)",
            (from_username, username),
        )

        conn_friends.commit()
        conn_friends.close()

    except Exception as e:
        conn_requests.rollback()
        conn_requests.close()
        logger.error(f"接受好友请求失败: {str(e)}")
        return jsonify({"error": "服务器内部错误"}), 500

    conn_requests.close()

    return jsonify({"message": "已接受好友请求"}), 200


@app.route(
    f"/api/{api_version}/friends/requests/<int:request_id>/reject", methods=["POST"]
)
def reject_friend_request(request_id):
    """
    拒绝好友请求
    API POST /friends/requests/<request_id>/reject
    请求体: {
        "token": "用户token"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不是JSON"}), 400

    token = data.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, username = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    conn_requests = get_friend_requests_db()
    friend_request = conn_requests.execute(
        "SELECT * FROM friend_requests WHERE id = ? AND status = 'pending'",
        (request_id,),
    ).fetchone()

    if not friend_request:
        conn_requests.close()
        return jsonify({"error": "好友请求不存在或已被处理"}), 404

    if friend_request["to_username"] != username:
        conn_requests.close()
        return jsonify({"error": "无权操作此好友请求"}), 403

    conn_requests.execute(
        """UPDATE friend_requests 
           SET status = 'rejected', updated_at = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (request_id,),
    )
    conn_requests.commit()
    conn_requests.close()

    return jsonify({"message": "已拒绝好友请求"}), 200


@app.route(f"/api/{api_version}/friends", methods=["GET"])
def get_friends_list():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, username = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 从 friends.db 获取好友列表
    conn_friend = get_friend_db()
    friend_rows = conn_friend.execute(
        "SELECT friend_username, created_at FROM friends WHERE username = ?", (username,)
    ).fetchall()
    conn_friend.close()

    # 获取每个好友的资料信息（可选）
    result = []
    conn_profile = get_user_profile_db()
    for row in friend_rows:
        friend_info = {
            "username": row["friend_username"],
            "created_at": row["created_at"],
        }

        # 获取好友昵称（如果有）
        profile = conn_profile.execute(
            "SELECT nickname FROM user_profiles WHERE username = ?",
            (row["friend_username"],)
        ).fetchone()
        if profile and profile["nickname"]:
            friend_info["nickname"] = profile["nickname"]

        result.append(friend_info)
    conn_profile.close()

    return jsonify({"friends": result}), 200


@app.route(f"/api/{api_version}/friends/<friend_username>", methods=["DELETE"])
def remove_friend(friend_username):
    """
    删除好友
    API DELETE /friends/<friend_username>
    请求体: {
        "token": "用户token"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不是JSON"}), 400

    token = data.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, username = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    conn = get_friend_db()
    # 删除双向好友关系
    conn.execute(
        "DELETE FROM friends WHERE (username = ? AND friend_username = ?) OR (username = ? AND friend_username = ?)",
        (username, friend_username, friend_username, username),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "好友已删除"}), 200


@app.route(f"/api/{api_version}/sessions", methods=["DELETE"])
def delete_session():
    """
    删除一个存在的token (api DELETE /sessions)
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不是JSON"}), 400

    token = data.get("token")
    if token_map.get(token) is None:
        return jsonify({"error": "token 失效"}), 401
    else:
        token_map.pop(token)

    return jsonify({"msg": "完成"}), 200


# ---------- 健康检查 ----------
@app.route(f"/api/{api_version}/health", methods=["GET"])
def health():
    """
    检查与服务器的链接 (api GET /health)
    """
    return jsonify({"error": "ok"}), 200


if __name__ == "__main__":
    create_rsa_key()
    app.run(host="127.0.0.1", port=5000, debug=True)