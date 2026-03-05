from PySide6.QtCore import QFile, QStringListModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QCommandLinkButton,
    QDialog,
    QDockWidget,
    QFrame,
    QLineEdit,
    QListView,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QToolButton,
    QWidget,
    QLabel,
    QPlainTextEdit
)

import add_friend
import search_users_ui
from client_api import (
    get_friends_list,
    login,
    register,
    search_users,
    send_friend_request,
)


class RegLogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action = ""
        self.logged_in = False
        self.password = ""
        self.user_name = ""
        self.token = ""


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
        self.listView.doubleClicked.connect(self.addFriends)

    def addFriends(self):
        window = addFriendWindow(self.token, self.listView.model().data(self.listView.currentIndex()))
        window.exec()

    def search(self):
        r = search_users(self.token, self.line_edit.text())
        self.listView.setModel(QStringListModel([]))
        if r.status_code == 200:
            self.listView.setModel(QStringListModel(r.json()["users"]))
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


class addFriendWindow(QDialog):
    def __init__(self, token, user_name):
        super().__init__()
        self.token = token
        self.user_name = user_name
        add_friend.Ui_Dialog().setupUi(self)
        self.label = self.findChild(
            QFrame, "frame").findChild(
            QLabel, "label"
        )
        self.label.setText(f"添加好友: {user_name}。请填写验证信息。")


        self.ok_b = self.findChild(
            QFrame, "frame_2").findChild(
            QPushButton, "pushButton"
        )
        self.no_b = self.findChild(
            QFrame, "frame_2").findChild(
            QPushButton, "pushButton_2"
        )

        self.no_b.clicked.connect(lambda : self.close())
        self.ok_b.clicked.connect(self.ok)

    def ok(self):
        r = send_friend_request(self.token, self.user_name, self.findChild(QFrame, "frame").findChild(QPlainTextEdit, "plainTextEdit").toPlainText())

        if r.status_code == 200:
            QMessageBox.information(None, "添加好友", "好友请求已发送!")
            self.close()
        elif r.status_code != 200 and r.status_code != -1:
            try:
                QMessageBox.warning(None, "添加好友", f"发生错误:{r.json()["error"]}")
            except:
                QMessageBox.warning(
                    None, "添加好友", f"发生错误，但服务器没有提供错误信息"
                )
        else:
            QMessageBox.warning(None, "添加好友", f"发生错误，无法跟服务器进行通讯")


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
        self.add_friend_button.clicked.connect(self.show_search_users_window)

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
            f"用户名: {r.get('username')}\n用户id: {r.get("user_id")} \n添加时间: {r.get("created_at")}\n",
        )


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
        chatting_window = ChattingWindow(
            login_window.password, login_window.user_name, login_window.token
        )
        chatting_window.window.show()
        app.exec()
