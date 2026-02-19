import pickle
import sys
from plistlib import load

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QLineEdit,
                               QMainWindow, QMessageBox, QPushButton)
from PySide6.scripts.metaobjectdump import Slot

from client_api import login, register


class RegLogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action = ""
        self.logged_in = False
        self.password = ""
        self.user_name = ""


class LoginWindow(RegLogWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("login.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        self.login_button = self.window.findChild(QPushButton, "login")
        self.login_button.clicked.connect(self.login)

        self.register_button = self.window.findChild(QCommandLinkButton, "register_2")
        self.register_button.clicked.connect(self.register)

        self.input_user_name = self.window.findChild(QLineEdit, "user_name")
        self.input_password = self.window.findChild(QLineEdit, "password")

        self.logged_in = False
        self.action = ""

    def login(self):
        r = login(self.input_user_name.text(), self.input_password.text())
        if r.status_code == 200:
            QMessageBox.information(None, "登录", "登录成功!")
            self.logged_in = True
            self.action = ""
            self.user_name = self.input_user_name.text()
            self.password = self.input_password.text()
        elif r.status_code != 200 and r.status_code != -1:
            try:
                QMessageBox.warning(None, "登录", f"发生错误:{r.json()["error"]}")
            except:
                QMessageBox.warning(None, "登录", f"发生错误，但服务器没有提供错误信息")
        else:
            QMessageBox.warning(None, "登录", f"发生错误，无法跟服务器进行通讯")

    def register(self):
        self.action = "register"
        self.window.close()


class RegisterWindow(RegLogWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("register.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        self.register_button = self.window.findChild(QPushButton, "register_2")
        self.register_button.clicked.connect(self.register)

        self.login_button = self.window.findChild(QCommandLinkButton, "login")
        self.login_button.clicked.connect(self.login)

        self.user_name = self.window.findChild(QLineEdit, "user_name")
        self.password = self.window.findChild(QLineEdit, "password")
        self.password_2 = self.window.findChild(QLineEdit, "password_2")

        self.logged_in = False
        self.action = ""

    def register(self):
        if self.password.text() == self.password_2.text():
            r = register(self.user_name.text(), self.password.text())
            if r.status_code == 201:
                QMessageBox.information(None, "注册", "注册成功! 请登录!")
                self.login()
            elif r.status_code != 201 and r.status_code != -1:
                try:
                    QMessageBox.warning(None, "注册", f"发生错误:{r.json()["error"]}")
                except:
                    QMessageBox.warning(
                        None, "注册", f"发生错误，但服务器没有提供错误信息"
                    )
            else:
                QMessageBox.warning(None, "注册", f"发生错误，无法跟服务器进行通讯")
        else:
            QMessageBox.warning(None, "注册", "两次输入的密码不一致")

    def login(self):
        self.action = "login"
        self.window.close()


if __name__ == "__main__":
    app = QApplication([])
    login_window: RegLogWindow = RegLogWindow()
    login_window.action = "login"
    while True:
        if login_window.action == "register":
            login_window = RegisterWindow()
            login_window.window.show()  # type: ignore[attr-defined]
        elif login_window.action == "login":
            login_window = LoginWindow()
            login_window.window.show()  # type: ignore[attr-defined]
        elif login_window.logged_in:
            break
        app.exec()
