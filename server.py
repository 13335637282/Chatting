import base64
import json
import logging
import os
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

token_map: dict = {}
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
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
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, friend_id)
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
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',  -- pending, accepted, rejected
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(from_user_id, to_user_id)
        )
    """)
    conn.commit()
    conn.close()


init_friend_db()
init_login_db()
init_friend_requests_db()


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


# ---------- 辅助函数 ----------
def verify_token(token: str) -> tuple:
    """
    验证token并返回用户名和用户信息
    返回: (is_valid, username, user_id)
    """
    if token_map.get(token) is None:
        return False, None, None

    username = token_map.get(token)
    conn = get_login_db()
    user = conn.execute(
        "SELECT id, username FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user:
        return True, username, user["id"]
    else:
        return False, None, None


def get_user_id_by_username(username: str) -> int:
    """通过用户名获取用户ID"""
    conn = get_login_db()
    user = conn.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user["id"] if user else None  # type: ignore[return-value]


def get_username_by_id(user_id: int) -> str:
    """通过用户ID获取用户名"""
    conn = get_login_db()
    user = conn.execute(
        "SELECT username FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user["username"] if user else None  # type: ignore[return-value]


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
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "用户名已存在"}), 409
    conn.close()

    return jsonify({"message": "用户创建成功"}), 201


@app.route(f"/api/{api_version}/users/<token>", methods=["GET"])
def get_user(token: str):
    """
    还在开发中的api 暂无文档
    """
    if token_map.get(token) is None:
        return jsonify({"error": "token 错误"}), 401
    else:
        username = token_map.get(token)
    conn = get_login_db()
    user = conn.execute(
        "SELECT id, username FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "用户不存在"}), 404


def random_token() -> str:
    """
    随机一个token,
    如果这个token已经被占用，就会重新 生成一个，直到生成一个未被占用的token
    构造函数：token = str(uuid.uuid5(uuid.uuid4(),str(uuid.uuid4())))
    """
    while True:
        token = str(uuid.uuid5(uuid.uuid4(), str(uuid.uuid4())))
        if token_map.get(token) is None:
            return str(token)


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
    is_valid, username, user_id = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 获取好友ID
    friend_id = get_user_id_by_username(friend_username)
    if not friend_id:
        return jsonify({"error": "好友用户不存在"}), 404

    # 不能添加自己为好友
    if user_id == friend_id:
        return jsonify({"error": "不能添加自己为好友"}), 400

    # 检查是否已经是好友
    conn = get_friend_db()
    existing_friend = conn.execute(
        "SELECT id FROM friends WHERE user_id = ? AND friend_id = ?",
        (user_id, friend_id),
    ).fetchone()
    if existing_friend:
        conn.close()
        return jsonify({"error": "已经是好友关系"}), 409

    # 检查是否已经存在好友请求
    conn_requests = get_friend_requests_db()
    existing_request = conn_requests.execute(
        """SELECT id, status FROM friend_requests 
           WHERE from_user_id = ? AND to_user_id = ?""",
        (user_id, friend_id),
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
            """INSERT INTO friend_requests (from_user_id, to_user_id, message)
               VALUES (?, ?, ?)""",
            (user_id, friend_id, message),
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

    is_valid, username, user_id = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 从 friend_requests.db 获取待处理的请求列表
    conn_req = get_friend_requests_db()
    requests = conn_req.execute(
        """SELECT id, from_user_id, message, status, created_at
           FROM friend_requests
           WHERE to_user_id = ? AND status = 'pending'
           ORDER BY created_at DESC""",
        (user_id,),
    ).fetchall()
    conn_req.close()

    # 从 login.db 获取每个请求发送者的用户名
    result = []
    conn_login = get_login_db()
    for req in requests:
        from_user = conn_login.execute(
            "SELECT username FROM users WHERE id = ?", (req["from_user_id"],)
        ).fetchone()
        if from_user:
            result.append(
                {
                    "request_id": req["id"],
                    "from_user_id": req["from_user_id"],
                    "from_username": from_user["username"],
                    "message": req["message"],
                    "created_at": req["created_at"],
                }
            )
    conn_login.close()

    return jsonify({"requests": result}), 200


@app.route(f"/api/{api_version}/friends/requests/outgoing", methods=["GET"])
def get_outgoing_requests():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "缺少token参数"}), 400

    is_valid, username, user_id = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 从 friend_requests.db 获取发出的请求列表
    conn_req = get_friend_requests_db()
    requests = conn_req.execute(
        """SELECT id, to_user_id, message, status, created_at
           FROM friend_requests
           WHERE from_user_id = ?
           ORDER BY created_at DESC""",
        (user_id,),
    ).fetchall()
    conn_req.close()

    # 从 login.db 获取每个接收者的用户名
    result = []
    conn_login = get_login_db()
    for req in requests:
        to_user = conn_login.execute(
            "SELECT username FROM users WHERE id = ?", (req["to_user_id"],)
        ).fetchone()
        if to_user:
            result.append(
                {
                    "request_id": req["id"],
                    "to_user_id": req["to_user_id"],
                    "to_username": to_user["username"],
                    "message": req["message"],
                    "status": req["status"],
                    "created_at": req["created_at"],
                }
            )
    conn_login.close()

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

    is_valid, username, user_id = verify_token(token)
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
    if friend_request["to_user_id"] != user_id:
        conn_requests.close()
        return jsonify({"error": "无权操作此好友请求"}), 403

    from_user_id = friend_request["from_user_id"]

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
            "INSERT OR IGNORE INTO friends (user_id, friend_id) VALUES (?, ?)",
            (user_id, from_user_id),
        )

        # 添加 B -> A 的关系
        conn_friends.execute(
            "INSERT OR IGNORE INTO friends (user_id, friend_id) VALUES (?, ?)",
            (from_user_id, user_id),
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

    is_valid, username, user_id = verify_token(token)
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

    if friend_request["to_user_id"] != user_id:
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

    is_valid, username, user_id = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    # 从 friends.db 获取好友ID列表
    conn_friend = get_friend_db()
    friend_rows = conn_friend.execute(
        "SELECT friend_id, created_at FROM friends WHERE user_id = ?", (user_id,)
    ).fetchall()
    conn_friend.close()

    # 从 login.db 获取每个好友的用户名
    result = []
    conn_login = get_login_db()
    for row in friend_rows:
        friend_id = row["friend_id"]
        user = conn_login.execute(
            "SELECT username FROM users WHERE id = ?", (friend_id,)
        ).fetchone()
        if user:
            result.append(
                {
                    "user_id": friend_id,
                    "username": user["username"],
                    "created_at": row["created_at"],
                }
            )
    conn_login.close()

    return jsonify({"friends": result}), 200


@app.route(f"/api/{api_version}/friends/<int:friend_id>", methods=["DELETE"])
def remove_friend(friend_id):
    """
    删除好友
    API DELETE /friends/<friend_id>
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

    is_valid, username, user_id = verify_token(token)
    if not is_valid:
        return jsonify({"error": "token无效或已过期"}), 401

    conn = get_friend_db()
    # 删除双向好友关系
    conn.execute(
        "DELETE FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)",
        (user_id, friend_id, friend_id, user_id),
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
