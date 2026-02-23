import base64
import logging

import requests  # type: ignore[import-untyped]
import rsa
from argon2 import PasswordHasher
from requests.models import Response  # type: ignore[import-untyped]
from rsa import PublicKey

BASE_URL = "http://127.0.0.1:5000/api/v1"
logger = logging.getLogger("client/api")
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s/%(name)s %(levelname)s]%(filename)s.%(funcName)s(%(lineno)s):\n %(message)s",
)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("client.log"))

__license__ = """Apache License 2.0"""


def rsa_encrypt(bytes_: bytes) -> bytes:
    """
    传入一个 bytes 对象输出一个使用 RSA公钥加密 后的 bytes 对象
    注意输出的 bytes 对象需使用 base64 编码后再和服务器端传输
    """
    with open("PUBLIC_KEY.chatting", "rb") as fread:
        pub_key = PublicKey.load_pkcs1(fread.read())
    cipher_bin = rsa.encrypt(bytes_, pub_key)
    return cipher_bin


def register(username: str, plain_password: str) -> Response:
    """
    传入 用户名 和 原密码 (未经处理的密码) ，函数会向服务器端发送 POST /users，
    请求体的password 对象会经过RSA加密和Base64编码，函数会返回服务器返回的 Response 对象。
    接口详细信息参阅 readme.md 文档
    注意：**如果向服务器请求失败，会返回一个状态码为-1的Response对象**
    """
    try:
        url = f"{BASE_URL}/users"
        logger.debug("[注册] 创建请求体中")
        payload = {
            "username": username,
            "password": base64.b64encode(
                rsa_encrypt(plain_password.encode("utf-8"))
            ).decode("utf-8"),
        }
        logger.debug(f"[注册] 请求中... 请求体: {payload}")
        resp: Response = requests.post(url, json=payload)
        logger.debug(
            f"[注册] {username} -> 状态 {resp.status_code}, 响应: {resp.json()}"
        )
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def login(username: str, plain_password: str) -> Response:
    """
    传入 用户名 和 原密码 (未经处理的密码) ，函数会向服务器端发送 POST /sessions，
    请求体的 password 对象会经过RSA加密和Base64编码，函数会返回服务器返回的 Response 对象。
    注意：**如果向服务器请求失败，会返回一个状态码为-1的Response对象**
    """
    try:
        logger.debug("[登录] 创建请求体中...")
        url = f"{BASE_URL}/sessions"
        payload = {
            "username": username,
            "password": base64.b64encode(
                rsa_encrypt(plain_password.encode("utf-8"))
            ).decode("utf-8"),
        }
        logger.debug(f"[登录] 请求中... Password:{payload}")
        resp: Response = requests.post(url, json=payload)
        logger.debug(
            f"[登录] {username} -> 状态 {resp.status_code}, 响应: {resp.json()}"
        )
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def get_user(token) -> Response:
    """
    此函数还在开发中...
    暂无文档
    """
    try:
        url = f"{BASE_URL}/users/{token}"
        resp: Response = requests.get(url)
        logger.debug(f"[查询] {token} -> 状态 {resp.status_code}, 响应: {resp.json()}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def logout(token) -> Response:
    """
    传入一个 token 服务器将会删除这个token。
    注意： 如果请求失败会返回一个状态码为 -1 的 Response 对象。
    """
    try:
        url = f"{BASE_URL}/sessions"
        payload = {"token": token}
        resp: Response = requests.delete(url, json=payload)
        logger.debug(f"[登出] {token} -> 状态 {resp.status_code}, 响应: {resp.json()}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def send_friend_request(
    token: str, friend_username: str, message: str = ""
) -> Response:
    """
    发送好友请求
    API POST /friends/requests
    """
    try:
        url = f"{BASE_URL}/friends/requests"
        payload = {
            "token": token,
            "friend_username": friend_username,
            "message": message,
        }
        logger.debug(f"[发送好友请求] 请求中... 好友: {friend_username}")
        resp: Response = requests.post(url, json=payload)
        logger.debug(f"[发送好友请求] -> 状态 {resp.status_code}, 响应: {resp.json()}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def get_incoming_requests(token: str) -> Response:
    """
    获取收到的好友请求
    API GET /friends/requests/incoming?token=<token>
    """
    try:
        url = f"{BASE_URL}/friends/requests/incoming"
        params = {"token": token}
        resp: Response = requests.get(url, params=params)
        logger.debug(f"[获取收到的请求] -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def get_outgoing_requests(token: str) -> Response:
    """
    获取发出的好友请求
    API GET /friends/requests/outgoing?token=<token>
    """
    try:
        url = f"{BASE_URL}/friends/requests/outgoing"
        params = {"token": token}
        resp: Response = requests.get(url, params=params)
        logger.debug(f"[获取发出的请求] -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def accept_friend_request(token: str, request_id: int) -> Response:
    """
    接受好友请求
    API POST /friends/requests/<request_id>/accept
    """
    try:
        url = f"{BASE_URL}/friends/requests/{request_id}/accept"
        payload = {"token": token}
        resp: Response = requests.post(url, json=payload)
        logger.debug(f"[接受好友请求] {request_id} -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def reject_friend_request(token: str, request_id: int) -> Response:
    """
    拒绝好友请求
    API POST /friends/requests/<request_id>/reject
    """
    try:
        url = f"{BASE_URL}/friends/requests/{request_id}/reject"
        payload = {"token": token}
        resp: Response = requests.post(url, json=payload)
        logger.debug(f"[拒绝好友请求] {request_id} -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def get_friends_list(token: str) -> Response:
    """
    获取好友列表
    API GET /friends?token=<token>
    """
    try:
        url = f"{BASE_URL}/friends"
        params = {"token": token}
        resp: Response = requests.get(url, params=params)
        logger.debug(f"[获取好友列表] -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def remove_friend(token: str, friend_id: int) -> Response:
    """
    删除好友
    API DELETE /friends/<friend_id>
    """
    try:
        url = f"{BASE_URL}/friends/{friend_id}"
        payload = {"token": token}
        resp: Response = requests.delete(url, json=payload)
        logger.debug(f"[删除好友] {friend_id} -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def get_user_info(token: str, username: str) -> Response:
    """
    获取用户详细信息（仅自己和好友可见）
    API GET /users/<username>?token=<token>

    参数:
        token: 当前登录用户的token
        username: 要查询的用户名

    返回:
        如果是自己或好友，返回用户详细信息（包含昵称、生日、邮箱等资料）
        如果是非好友，返回403错误
    """
    try:
        url = f"{BASE_URL}/users/{username}"
        params = {"token": token}
        resp: Response = requests.get(url, params=params)
        logger.debug(f"[获取用户信息] {username} -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep

def update_user_profile(token: str, username: str, **kwargs) -> Response:
    """
    更新用户资料
    API PUT /users/<username>/profile

    参数:
        token: 当前登录用户的token
        username: 要更新资料的用户名（必须是自己）
        **kwargs: 可更新的字段
            - nickname: 昵称
            - birthday: 生日 (格式: YYYY-MM-DD)
            - gender: 性别 (male/female/other)
            - avatar: 头像 (base64编码的图片数据)
            - email: 邮箱
            - phone: 电话
            - bio: 个人简介

    示例:
        update_user_profile(token, "alice", nickname="爱丽丝", bio="Hello World")
    """
    try:
        url = f"{BASE_URL}/users/{username}/profile"
        payload = {"token": token}
        # 添加所有提供的资料字段
        for key, value in kwargs.items():
            if value is not None:  # 只添加有值的字段
                payload[key] = value

        logger.debug(f"[更新用户资料] {username} -> 字段: {list(kwargs.keys())}")
        resp: Response = requests.put(url, json=payload)
        logger.debug(f"[更新用户资料] -> 状态 {resp.status_code}, 响应: {resp.json()}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def rename_user(token: str, old_username: str, new_username: str) -> Response:
    """
    修改用户名
    API PUT /users/<old_username>/rename

    参数:
        token: 当前登录用户的token
        old_username: 当前用户名
        new_username: 新用户名（至少3个字符）

    注意:
        修改用户名后，所有相关数据（好友关系、好友请求、用户资料）都会自动更新，
        当前的token仍然有效（会自动关联到新用户名）
    """
    try:
        url = f"{BASE_URL}/users/{old_username}/rename"
        payload = {
            "token": token,
            "new_username": new_username
        }
        logger.debug(f"[修改用户名] {old_username} -> {new_username}")
        resp: Response = requests.put(url, json=payload)
        logger.debug(f"[修改用户名] -> 状态 {resp.status_code}, 响应: {resp.json()}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


def search_users(token: str, query: str) -> Response:
    """
    搜索用户
    API GET /users/search?q=<query>&token=<token>

    参数:
        token: 当前登录用户的token
        query: 搜索关键词（至少2个字符）

    返回:
        {
            "users": ["username1", "username2", ...]
        }

    注意:
        搜索结果不包含自己，最多返回50个结果
    """
    try:
        url = f"{BASE_URL}/users/search"
        params = {
            "token": token,
            "q": query
        }
        logger.debug(f"[搜索用户] 关键词: {query}")
        resp: Response = requests.get(url, params=params)
        logger.debug(
            f"[搜索用户] -> 状态 {resp.status_code}, 找到: {len(resp.json().get('users', [])) if resp.status_code == 200 else 0} 个用户")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


if __name__ == "__main__":
    print("client_api.py 并不是一个运行执行代码的文件，如需访问功能，请参阅 readme.md")
