import pickle
import sys
from plistlib import load

import search_friends_ui
from PySide6.QtCore import QFile, QIODevice, QStringListModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QLineEdit,
                               QMainWindow, QMessageBox, QPushButton, QScrollArea, QLabel, QDockWidget, QWidget,
                               QFrame, QListView, QTableWidget, QTableWidgetItem, QToolButton, QDialog)
from PySide6.scripts.metaobjectdump import Slot

from client_api import (login, register, get_friends_list, get_incoming_requests,
                        get_outgoing_requests, get_user, logout, logger, search_users, get_user_info, rename_user)


class RegLogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action = ""
        self.logged_in = False
        self.password = ""
        self.user_name = ""
        self.token = ""

class SearchFriendWindow(QDialog):
    def __init__(self, token):
        super().__init__()
        self.token = token

        search_friends_ui.Ui_Dialog().setupUi(self)


    def search(self):
        r = search_users(self.token, self.input_user_name.text())
        if r.status_code == 200:
            QMessageBox.information(None, "搜索", f"用户信息:\n用户名: {r.json().get('username')}\n用户id: {r.json().get('user_id')}\n注册时间: {r.json().get('created_at')}")
        elif r.status_code != 200 and r.status_code != -1:
            try:
                QMessageBox.warning(None, "搜索", f"发生错误:{r.json()["error"]}")
            except:
                QMessageBox.warning(None, "搜索", f"发生错误，但服务器没有提供错误信息")
        else:
            QMessageBox.warning(None, "搜索", f"发生错误，无法跟服务器进行通讯")

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
            self.token = r.json().get("token")
            self.window.close()
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


class ChattingWindow(QMainWindow):
    def __init__(self, password, user_name, token):
        super().__init__()

        self.password = password
        self.user_name = user_name
        self.token = token

        loader = QUiLoader()
        ui_file = QFile("chatting_main.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        self.friends_list_data = self.reload_friends_list()

        self.friends_list = (self.window
                             .findChild(QDockWidget, "dockWidget_4")
                             .findChild(QWidget, "dockWidgetContents_5")
                             .findChild(QListView, "friends_list"))
        self.friends_list.doubleClicked.connect(self.show_info)

        self.search_friend_button = (self.window
                                     .findChild(QDockWidget, "dockWidget_4")
                                     .findChild(QWidget, "dockWidgetContents_5")
                                     .findChild(QFrame, "frame_2")
                                     .findChild(QToolButton, "search")
                                     )
        self.search_friend_button.clicked.connect(self.show_search_friend_window)


    def show_search_friend_window(self):
        search_friend_window = SearchFriendWindow(self.token)
        search_friend_window.exec()


    def reload_friends_list(self) ->  list[str]:
        friends_list = (self.window
                             .findChild(QDockWidget, "dockWidget_4")
                             .findChild(QWidget, "dockWidgetContents_5")
                             .findChild(QListView, "friends_list"))
        friends_list.setModel(QStringListModel([]))

        friends_list_temp = []
        friends_list_r = get_friends_list(self.token)
        self.friends_list_data = friends_list_r.json()
        if friends_list_r.status_code == 200:
            friends_list_l = QStringListModel()
            for i in friends_list_r.json().get("friends"):
                friends_list_temp.append(i.get("username"))
            friends_list_temp.sort()
            friends_list_l .setStringList(friends_list_temp)
            friends_list.setModel(friends_list_l)
        else:
            QMessageBox.warning(None, "获取好友列表", f"发生错误，无法跟服务器进行通讯")
        return friends_list_r.json()

    def show_info(self):
        r = self.friends_list_data.get("friends")[self.friends_list.currentIndex().row()]
        QMessageBox.information(None, "好友", f"用户名: {r.get('username')}\n用户id: {r.get("user_id")} \n添加时间: {r.get("created_at")}\n")

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
            app.quit()
            break
        else:
            app.quit()
            break
        app.exec()


    if login_window.logged_in:
        chatting_window = ChattingWindow(login_window.password, login_window.user_name, login_window.token)
        chatting_window.window.show()
        app.exec()
