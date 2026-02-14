import hashlib
import logging
from pickle import OBJ
from threading import Thread
from typing import Literal

import requests  # type: ignore[import-untyped]

import rich
from requests.models import Response  # type: ignore[import-untyped]
from textual import on
from textual.app import ComposeResult, App
from textual.widgets import Footer, Header, Button, Input, ListView, Label, ListItem
from textual.containers import Container

from logger import Logger  # type: ignore[attr-defined]

BASE_URL = 'http://127.0.0.1:5000/api/v1'
logger = Logger("client/root","client.log","ZERO",mask_tokens=True)

def debug_print(*args:object):
    logger.debug(' '.join(str(arg) for arg in args))

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


# 1. 注册用户（RESTful POST /users）
def register(username, plain_password) -> Response:
    try:
        url = f'{BASE_URL}/users'
        payload = {
            'username': username,
            'password_hash': sha256(plain_password)
        }
        resp :Response = requests.post(url, json=payload)
        debug_print(f'[注册] {username} -> 状态 {resp.status_code}, 响应: {resp.json()}')
        return resp
    except Exception:
        rep: Response = Response()
        rep.status_code = -1
        return rep


# 2. 登录（RESTful POST /sessions）
def login(username, plain_password) -> Response:
    try:
        url = f'{BASE_URL}/sessions'
        payload = {
            'username': username,
            'password_hash': sha256(plain_password)
        }
        resp: Response = requests.post(url, json=payload)
        debug_print(f'[登录] {username} -> 状态 {resp.status_code}, 响应: {resp.json()}')
        return resp
    except Exception:
        rep:Response = Response()
        rep.status_code = -1
        return rep


# 3. 获取用户信息（RESTful GET /users/<token>）
def get_user(token) -> Response:
    try:
        url = f'{BASE_URL}/users/{token}'
        resp : Response = requests.get(url)
        debug_print(f'[查询] {token} -> 状态 {resp.status_code}, 响应: {resp.json()}')
        return resp
    except Exception:
        rep:Response = Response()
        rep.status_code = -1
        return rep

def logout(token) -> Response:
    try:
        url = f'{BASE_URL}/sessions'
        payload = {
            'token': token
        }
        resp: Response = requests.delete(url, json=payload)
        debug_print(f'[登出] {token} -> 状态 {resp.status_code}, 响应: {resp.json()}')
        return resp
    except Exception:
        rep:Response = Response()
        rep.status_code = -1
        return rep


if __name__ == '__main__':
    print("Loading...")

    class LoginApp(App):
        CSS_PATH = "login.css"
        ENABLE_COMMAND_PALETTE = False  # Do not need the command palette
        BINDINGS = [("d", "toggle_dark", "暗色主题切换"), ("q", "quit_app", "退出程序")]
        user_id:str = ""
        password:str = ""
        loggedin:bool = False
        token:str = ""

        def action_quit_app(self) -> None:
            self.exit()

        def compose(self) -> ComposeResult:
             # Create a list of commands, valid commands are assumed to be on the PATH variable.
            yield Header(show_clock=False)
            with Container(id="main_container"):
                yield Input("",id="user_id", placeholder="用户名/ID")
                yield Input("",id="user_password", placeholder="密码",password=True)
                yield Button(f"登录/注册", id="register", variant="primary")
                yield Footer()

        def login(self):
            r:Response =  login(username=self.user_id, plain_password=self.password)  # type: ignore[annotation-unchecked]
            if r.status_code == 200:
                self.clear_notifications()
                self.notify("登录成功!")
                self.query_one("#user_id").remove()
                self.query_one("#user_password").remove()
                self.query_one("#register").remove()
                self.loggedin = True
                self.token = r.json().get("token")
                self.exit()
                self.refresh(layout=True,repaint=True,recompose=True)
                self.compose_add_child()

            elif r.status_code != 200 and r.status_code != -1:
                self.notify(message=str(r.json().get("error"))+"("+str(r.status_code)+")",severity="error",title="错误")
            else:
                self.notify("链接服务器失败!",severity="error",title="错误")
            self.query_one("#register").disabled = False

        def register(self):
            r:Response =  register(username=self.user_id, plain_password=self.password)  # type: ignore[annotation-unchecked]
            if r.status_code == 201:
                self.notify("注册成功! 正在登录中...")
                self.login()
            elif r.status_code != 200 and r.status_code != 409 and r.status_code != -1:
                self.notify(message=str(r.json().get("error")),severity="error",title="错误")
            elif r.status_code == 409:
                self.login()
            else:
                self.notify("链接服务器失败!",severity="error",title="错误")
            self.query_one("#register").disabled = False

        @on(Button.Pressed, "#register")
        def register_pressed(self) -> None:
            self.query_one("#register").disabled = True
            Thread(target=self.register, daemon=True).start()

        def action_toggle_dark(self) -> None:
            """An action to toggle dark mode."""
            self.theme = (
                "textual-dark" if self.theme == "textual-light" else "textual-light"
            )

        @on(Input.Changed,"#user_id")
        def changed_user_id(self, event: Input.Changed) -> None:
            self.user_id = event.value

        @on(Input.Changed,"#user_password")
        def changed_user_password(self, event: Input.Changed) -> None:
            self.password = event.value

    class ChattingApp(App):
        CSS_PATH = "login.css"
        ENABLE_COMMAND_PALETTE = False  # Do not need the command palette
        BINDINGS = [("d", "toggle_dark", "暗色主题切换"), ("q", "quit_app", "退出程序")]
        user_id:str = ""
        password:str = ""
        token:str = ""
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
        app = LoginApp()
        app.title = f"登录".title()
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

