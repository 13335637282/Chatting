import os
import threading

import requests  # type: ignore[import-untyped]
from requests.models import Response  # type: ignore[import-untyped]
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Input, Label

from client_api import *

if __name__ == "__main__":
    print("Loading...")

    class LoginApp(App):  # type: ignore[no-redef]
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

    class ChattingApp(App):  # type: ignore[no-redef]
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
            logger.error(
                "缺少 RSA公钥 程序无法运行，请找服务端索要公钥。警告：不要修改文件。"
            )
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
