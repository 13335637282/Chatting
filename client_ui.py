import sys
import threading
import time
from threading import Thread

from PySide6.QtCore import QFile, QStringListModel, Qt, QThread
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QDialog,
                               QDockWidget, QFrame, QLabel, QLineEdit,
                               QListView, QMainWindow, QMessageBox,
                               QPlainTextEdit, QPushButton, QToolButton,
                               QWidget, QScrollArea, QVBoxLayout, )

import add_friend
import friend_request_widget
import request_manage
import search_users_ui
import schedule
from client_api import (get_friends_list, login, register, search_users,
                        send_friend_request, get_incoming_requests, get_outgoing_requests, accept_friend_request,
                        reject_friend_request, logout)

print("""
 ██████╗██╗  ██╗ █████╗ ████████╗████████╗██╗███╗   ██╗ ██████╗ 
██╔════╝██║  ██║██╔══██╗╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ 
██║     ███████║███████║   ██║      ██║   ██║██╔██╗ ██║██║  ███╗
██║     ██╔══██║██╔══██║   ██║      ██║   ██║██║╚██╗██║██║   ██║
╚██████╗██║  ██║██║  ██║   ██║      ██║   ██║██║ ╚████║╚██████╔╝
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ 

     _/_/_/  _/                    _/      _/      _/                      
  _/        _/_/_/      _/_/_/  _/_/_/_/_/_/_/_/      _/_/_/      _/_/_/   
 _/        _/    _/  _/    _/    _/      _/      _/  _/    _/  _/    _/    
_/        _/    _/  _/    _/    _/      _/      _/  _/    _/  _/    _/     
 _/_/_/  _/    _/    _/_/_/      _/_/    _/_/  _/  _/    _/    _/_/_/      
                                                                  _/       
                                                             _/_/          
""")

task = []

class RegLogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action = ""
        self.logged_in = False
        self.password = ""
        self.user_name = ""
        self.token = ""


class RequestWidget(QWidget):
    def __init__(self, token, username, content,request_id:int=None,state:str=None):
        super().__init__()
        self.token = token
        self.username = username
        self.content = content
        self.request_id = request_id
        friend_request_widget.Ui_Form().setupUi(self)
        self.findChild(QFrame,"frame_3").findChild(QLabel,"label").setText(username)
        self.findChild(QFrame,"frame_3").findChild(QLabel,"label_2").setText(content)
        if request_id:
            self.findChild(QToolButton, "toolButton").clicked.connect(self.accept)
            self.findChild(QToolButton, "toolButton_2").clicked.connect(self.reject)
        else:
            self.findChild(QToolButton, "toolButton").setEnabled(False)
            self.findChild(QToolButton, "toolButton").setText(state)
            self.findChild(QToolButton, "toolButton_2").setEnabled(False)
            self.findChild(QToolButton, "toolButton_2").hide()

    def accept(self):
        accept_friend_request(self.token, self.request_id)
        task.append("reload_friends_list")
        task.append("reload_request_list")

    def reject(self):
        reject_friend_request(self.token, self.request_id)
        task.append("reload_friends_list")
        task.append("reload_request_list")

class FriendsRequestManage(QDialog):
    def __init__(self, token):
        super().__init__()
        request_manage.Ui_Dialog().setupUi(self)
        self.scroll_area = self.findChild(QScrollArea, "scrollArea")

        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 竖向滚动条按需显示
        self.scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        # 设置布局间距和边距，优化显示效果
        self.content_layout.setSpacing(15)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        incoming = get_incoming_requests(token)
        outgoing = get_outgoing_requests(token)

        if (incoming.status_code == 200):
            for i in incoming.json()["requests"]:
                self.content_layout.addWidget(RequestWidget(token,i["from_username"],i["message"],i["request_id"]))

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.content_layout.addWidget(line)

        if (outgoing.status_code == 200):
            for i in outgoing.json()["requests"]:
                self.content_layout.addWidget(RequestWidget(token,i["to_username"],i["message"],
                                                            state=str(i["status"])
                                                            .replace("pending", "等待处理中")
                                                            .replace("accepted", "对方已通过")
                                                            .replace("rejected", "对方已拒绝")))


        self.scroll_area.setWidget(content_widget)


class SearchUsersWindow(QDialog):
    def __init__(self, token):
        super().__init__()
        self.token = token

        search_users_ui.Ui_Dialog().setupUi(self)
        self.search_button = self.findChild(QFrame, "frame_2").findChild(
            QToolButton, "toolButton"
        )
        self.search_button.clicked.connect(self.search)

        self.line_edit = self.findChild(QFrame, "frame_2").findChild(
            QLineEdit, "lineEdit"
        )
        self.listView = self.findChild(QListView, "listView")
        self.listView.doubleClicked.connect(self.add_friends)

        self.request_list_button = self.findChild(QFrame, "frame_2").findChild(
            QToolButton, "toolButton_2"
        )
        self.request_list_button.clicked.connect(self.request_manage)

    def request_manage(self):
        FriendsRequestManage(self.token).exec()

    def add_friends(self):
        window = addFriendWindow(
            self.token, self.listView.model().data(self.listView.currentIndex())
        )
        window.exec()

    def search(self):
        r = search_users(self.token, self.line_edit.text())
        self.listView.setModel(QStringListModel([]))
        if r.status_code == 200:
            self.listView.setModel(QStringListModel(r.json()["users"]))
        elif r.status_code != 200 and r.status_code != -1:
            try:
                QMessageBox.warning(None, "搜索", f"发生错误:{r.json()['error']}")
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
                QMessageBox.warning(None, "登录", f"发生错误:{r.json()['error']}")
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
                    QMessageBox.warning(None, "注册", f"发生错误:{r.json()['error']}")
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


class addFriendWindow(QDialog):
    def __init__(self, token, user_name):
        super().__init__()
        self.token = token
        self.user_name = user_name
        add_friend.Ui_Dialog().setupUi(self)
        self.label = self.findChild(QFrame, "frame").findChild(QLabel, "label")
        self.label.setText(f"添加好友: {user_name}。请填写验证信息。")

        self.ok_b = self.findChild(QFrame, "frame_2").findChild(
            QPushButton, "pushButton"
        )
        self.no_b = self.findChild(QFrame, "frame_2").findChild(
            QPushButton, "pushButton_2"
        )

        self.no_b.clicked.connect(lambda: self.close())
        self.ok_b.clicked.connect(self.ok)

    def ok(self):
        r = send_friend_request(
            self.token,
            self.user_name,
            self.findChild(QFrame, "frame")
            .findChild(QPlainTextEdit, "plainTextEdit")
            .toPlainText(),
        )

        if r.status_code == 201:
            QMessageBox.information(None, "添加好友", "好友请求已发送!")
            self.close()
        elif r.status_code != 201 and r.status_code != -1:
            try:
                QMessageBox.warning(None, "添加好友", f"发生错误:{r.json()['error']}")
            except:
                QMessageBox.warning(
                    None, "添加好友", f"发生错误，但服务器没有提供错误信息"
                )
        else:
            QMessageBox.warning(None, "添加好友", f"发生错误，无法跟服务器进行通讯")


class ChattingWindow(QMainWindow):
    def __init__(self, password, user_name, token):
        super().__init__()

        self.state = ""
        self.password = password
        self.user_name = user_name
        self.token = token

        loader = QUiLoader()
        ui_file = QFile("chatting_main.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        self.friends_list_data = self.reload_friends_list()

        self.friends_list = (
            self.window.findChild(QDockWidget, "dockWidget_4")
            .findChild(QWidget, "dockWidgetContents_5")
            .findChild(QListView, "friends_list")
        )
        self.friends_list.doubleClicked.connect(self.show_info)

        self.add_friend_button = (
            self.window.findChild(QDockWidget, "dockWidget_4")
            .findChild(QWidget, "dockWidgetContents_5")
            .findChild(QFrame, "frame_2")
            .findChild(QToolButton, "add_friends")
        )

        (
            self.window.findChild(QDockWidget, "dockWidget_4")
        .findChild(QWidget, "dockWidgetContents_5")
        .findChild(QFrame, "frame")
        .findChild(QToolButton, "toolButton_3")
        ).clicked.connect(self.logout)

        self.add_friend_button.clicked.connect(self.show_search_users_window)

        threading.Timer(0.2, self.scan_self_task).start()

    def scan_self_task(self):
        for i in task:
            if i == "reload_friends_list":
                self.reload_friends_list()
                task.remove(i)
        threading.Timer(0.2, self.scan_self_task).start()

    def logout(self):
        self.close()
        logout(self.token)
        self.state = "logout"

    def show_search_users_window(self):
        search_users_window = SearchUsersWindow(self.token)
        search_users_window.exec()

    def reload_friends_list(self) -> list[str]:
        friends_list = (
            self.window.findChild(QDockWidget, "dockWidget_4")
            .findChild(QWidget, "dockWidgetContents_5")
            .findChild(QListView, "friends_list")
        )
        friends_list.setModel(QStringListModel([]))

        friends_list_temp = []
        friends_list_r = get_friends_list(self.token)
        self.friends_list_data = friends_list_r.json()
        if friends_list_r.status_code == 200:
            friends_list_l = QStringListModel()
            for i in friends_list_r.json().get("friends"):
                friends_list_temp.append(i.get("username"))
            friends_list_temp.sort()
            friends_list_l.setStringList(friends_list_temp)
            friends_list.setModel(friends_list_l)
        else:
            QMessageBox.warning(None, "获取好友列表", f"发生错误，无法跟服务器进行通讯")
        return friends_list_r.json()

    def show_info(self):
        r = self.friends_list_data.get("friends")[
            self.friends_list.currentIndex().row()
        ]
        QMessageBox.information(
            None,
            "好友",
            f"用户名: {r.get('username')}\n用户id: {r.get('user_id')} \n添加时间: {r.get('created_at')}\n",
        )


def run_auth_flow():
    """运行登录/注册认证流程"""
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("ico.png"))
    auth_window = RegLogWindow()
    auth_window.action = "login"  # 默认进入登录流程

    # 核心认证循环：处理登录/注册切换
    while True:
        current_window = None

        # 根据操作类型创建对应窗口
        if auth_window.action == "register":
            current_window = RegisterWindow()
        elif auth_window.action == "login":
            current_window = LoginWindow()
        else:
            # 非登录/注册操作，退出认证流程
            break

        # 显示窗口并运行事件循环
        current_window.window.show()
        app.exec()

        # 更新认证窗口状态（继承当前窗口的状态）
        auth_window = current_window

        # 登录成功则进入聊天窗口
        if auth_window.logged_in:
            # 启动聊天窗口
            chatting_window = ChattingWindow(
                auth_window.password,
                auth_window.user_name,
                auth_window.token
            )
            chatting_window.window.show()
            app.exec()
            if (chatting_window.state == "logout"):
                pass
            else:
                break  # 聊天窗口退出后，结束整个认证流

    # 退出应用
    app.quit()


if __name__ == "__main__":
    # 主循环：支持关闭后重新打开认证窗口
    while True:
        run_auth_flow()

        exit_flag = False
        if exit_flag:
            exit(0)