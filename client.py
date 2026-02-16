import base64
import os
import threading

import requests  # type: ignore[import-untyped]
import rsa
from argon2 import PasswordHasher
from requests.models import Response  # type: ignore[import-untyped]
from rsa import PublicKey
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Input, Label

from logger import Logger

BASE_URL = "http://127.0.0.1:5000/api/v1"
logger = Logger("client/root", "client.log", "ZERO", mask_tokens=True)
ph = PasswordHasher()

__license__ = """Apache License 2.0"""


def debug_print(*args: object):
    """
    *args: 一个object对象，每个 arg 输出时会在中间空一个空格
    debug_print("1",1) 会往client.log 输出日志 "1 1"
    如果文件写入被系统中断 (OSError) 会予以静默处理
    """
    try:
        logger.debug(" ".join(str(arg) for arg in args))
    except OSError:
        pass


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
        debug_print("[注册] 创建请求体中")
        payload = {
            "username": username,
            "password": base64.b64encode(
                rsa_encrypt(plain_password.encode("utf-8"))
            ).decode("utf-8"),
        }
        debug_print(f"[注册] 请求中... 请求体: {payload}")
        resp: Response = requests.post(url, json=payload)
        debug_print(f"[注册] {username} -> 状态 {resp.status_code}, 响应: {resp.json()}")
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
        debug_print("[登录] 创建请求体中...")
        url = f"{BASE_URL}/sessions"
        payload = {
            "username": username,
            "password": base64.b64encode(
                rsa_encrypt(plain_password.encode("utf-8"))
            ).decode("utf-8"),
        }
        debug_print(f"[登录] 请求中... Password:{payload}")
        resp: Response = requests.post(url, json=payload)
        debug_print(f"[登录] {username} -> 状态 {resp.status_code}, 响应: {resp.json()}")
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
        debug_print(f"[查询] {token} -> 状态 {resp.status_code}, 响应: {resp.json()}")
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
        debug_print(f"[登出] {token} -> 状态 {resp.status_code}, 响应: {resp.json()}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep

def send_friend_request(token: str, friend_username: str, message: str = "") -> Response:
    """
    发送好友请求
    API POST /friends/requests
    """
    try:
        url = f"{BASE_URL}/friends/requests"
        payload = {
            "token": token,
            "friend_username": friend_username,
            "message": message
        }
        debug_print(f"[发送好友请求] 请求中... 好友: {friend_username}")
        resp: Response = requests.post(url, json=payload)
        debug_print(f"[发送好友请求] -> 状态 {resp.status_code}, 响应: {resp.json()}")
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
        debug_print(f"[获取收到的请求] -> 状态 {resp.status_code}")
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
        debug_print(f"[获取发出的请求] -> 状态 {resp.status_code}")
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
        debug_print(f"[接受好友请求] {request_id} -> 状态 {resp.status_code}")
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
        debug_print(f"[拒绝好友请求] {request_id} -> 状态 {resp.status_code}")
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
        debug_print(f"[获取好友列表] -> 状态 {resp.status_code}")
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
        debug_print(f"[删除好友] {friend_id} -> 状态 {resp.status_code}")
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep

if __name__ == "__main__":
    print("Loading...")


    class LoginApp(App):
        CSS_PATH = "login.css"
        ENABLE_COMMAND_PALETTE = False  # Do not need the command palette
        BINDINGS = [("d", "toggle_dark", "暗色主题切换"), ("q", "quit_app", "退出程序")]
        user_id: str = ""
        password: str = ""
        loggedin: bool = False
        token: str = ""

        def action_quit_app(self) -> None:
            self.exit()

        def compose(self) -> ComposeResult:
            # Create a list of commands, valid commands are assumed to be on the PATH variable.
            yield Header(show_clock=False)
            with Container(id="main_container"):
                yield Input("", id="user_id", placeholder="用户名/ID")
                yield Input("", id="user_password", placeholder="密码", password=True)
                yield Button("登录/注册", id="register", variant="primary")
                yield Footer()

        def login(self):
            r: Response = login(  # type: ignore[annotation-unchecked]
                username=self.user_id, plain_password=self.password
            )
            if r.status_code == 200:
                self.clear_notifications()
                self.notify("登录成功!")
                self.query_one("#user_id").remove()
                self.query_one("#user_password").remove()
                self.query_one("#register").remove()
                self.loggedin = True
                self.token = r.json().get("token")
                debug_print(f"返回 Token {self.token}")
                self.exit()
            elif r.status_code != 200 and r.status_code != -1:
                self.notify(
                    message=str(r.json().get("error")) + "(" + str(r.status_code) + ")",
                    severity="error",
                    title="错误",
                )
            else:
                debug_print(f"服务器连接失败，返回值: {r.status_code} (应为-1)")
                self.notify("链接服务器失败!", severity="error", title="错误")
            self.query_one("#register").disabled = False

        def register(self):
            r: Response = register(  # type: ignore[annotation-unchecked]
                username=self.user_id, plain_password=self.password
            )
            if r.status_code == 201:
                self.notify("注册成功! 正在登录中...")
                self.login()
            elif r.status_code != 200 and r.status_code != 409 and r.status_code != -1:
                self.notify(
                    message=str(r.json().get("error")), severity="error", title="错误"
                )
            elif r.status_code == 409:
                self.login()
            else:
                self.notify("链接服务器失败!", severity="error", title="错误")
            self.query_one("#register").disabled = False

        @on(Button.Pressed, "#register")
        def register_pressed(self) -> None:
            self.query_one("#register").disabled = True
            threading.Thread(target=self.register, daemon=True).start()

        def action_toggle_dark(self) -> None:
            """An action to toggle dark mode."""
            self.theme = (
                "textual-dark" if self.theme == "textual-light" else "textual-light"
            )

        @on(Input.Changed, "#user_id")
        def changed_user_id(self, event: Input.Changed) -> None:
            self.user_id = event.value

        @on(Input.Changed, "#user_password")
        def changed_user_password(self, event: Input.Changed) -> None:
            self.password = event.value


    class ChattingApp(App):
        CSS_PATH = "login.css"
        ENABLE_COMMAND_PALETTE = False  # Do not need the command palette
        BINDINGS = [("d", "toggle_dark", "暗色主题切换"), ("q", "quit_app", "退出程序")]
        user_id: str = ""
        password: str = ""
        token: str = ""
        exit_action = "none"

        def compose(self) -> ComposeResult:
            # Create a list of commands, valid commands are assumed to be on the PATH variable.
            yield Header(show_clock=False)
            with Container(id="main_container"):
                yield Label(str(self.token))
            yield Footer()

        def action_quit_app(self) -> None:
            logout(token=self.token)
            self.exit()

        def action_toggle_dark(self) -> None:
            """An action to toggle dark mode."""
            self.theme = (
                "textual-dark" if self.theme == "textual-light" else "textual-light"
            )


    def main():
        if not os.path.exists("PUBLIC_KEY.chatting"):
            logger.error("缺少 RSA公钥 程序无法运行，请找服务端索要公钥。警告：不要修改文件。")
            print("缺少 RSA公钥 程序无法运行，请找服务端索要公钥。警告：不要修改文件。")
            exit(-1)
        try:
            rsa_encrypt(b"test")
        except Exception:
            logger.error("无法使用 rsa 功能请检查 PUBLIC_KEY.chatting 文件")
            print("无法使用 rsa 功能请检查 PUBLIC_KEY.chatting 文件")
            exit(-1)
        app = LoginApp()
        app.title = "登录".title()
        app.run()

        if app.loggedin and app.token is not None:
            print("登录成功")
            chatting = ChattingApp()
            chatting.user_id = app.user_id
            chatting.password = app.password
            chatting.token = app.token
            chatting.run()
        else:
            print("登录失败")


    main()