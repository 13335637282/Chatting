import json
import os
import sys
import threading
from threading import Thread

import schedule
from PySide6.QtCore import QFile, QStringListModel, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QFontDatabase, QIcon, QPalette
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QComboBox, QCommandLinkButton,
                               QDialog, QDockWidget, QFileDialog, QFrame,
                               QLabel, QLineEdit, QListView, QMainWindow,
                               QMessageBox, QPlainTextEdit, QPushButton,
                               QRadioButton, QScrollArea, QSpinBox,
                               QTextBrowser, QToolButton, QVBoxLayout, QWidget)

import add_friend
import friend_request_widget
import request_manage
import search_users_ui
import settings
from client_api import (accept_friend_request, get_friends_list,
                        get_incoming_requests, get_outgoing_requests, login,
                        logout, register, reject_friend_request, search_users,
                        send_friend_request)

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

# 全局任务队列（所有操作在主线程处理，故无需锁）
task = []


def get_setting(path, default=None):
    """读取配置文件 settings.json，获取指定路径的值

    Args:
        path: 配置项路径，支持点号分隔的嵌套路径，如 "user.name"
        default: 默认值，如果配置不存在则返回此值

    Returns:
        配置值或默认值
    """
    settings_file = "settings.json"

    # 如果文件不存在，创建空配置文件
    if not os.path.exists(settings_file):
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return default

    # 读取配置文件
    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except (json.JSONDecodeError, IOError):
        # 文件损坏或读取失败，创建新文件
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return default

    # 按路径获取值
    keys = path.split(".")
    value = settings
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value


def set_setting(path, value):
    """设置配置文件中指定路径的值

    Args:
        path: 配置项路径，支持点号分隔的嵌套路径，如 "user.name"
        value: 要设置的值

    Returns:
        bool: 是否设置成功
    """
    settings_file = "settings.json"

    # 读取现有配置
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, IOError):
            settings = {}
    else:
        settings = {}

    # 按路径设置值
    keys = path.split(".")
    current = settings
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

    # 写入文件
    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False


def show_api_error(parent, context, response):
    """统一显示API错误信息"""
    if response.status_code == -1:
        QMessageBox.warning(parent, context, "发生错误，无法与服务器进行通讯")
    else:
        try:
            error_msg = response.json().get("error", "未知错误")
        except Exception:
            error_msg = "服务器返回了无法解析的响应"
        QMessageBox.warning(parent, context, f"错误: {error_msg}")


class RegLogWindow(QMainWindow):
    """登录/注册基类（保留以兼容现有逻辑）"""

    def __init__(self):
        super().__init__()
        self.action = ""
        self.logged_in = False
        self.password = ""
        self.user_name = ""
        self.token = ""


class FriendRequestManageDialog_(QDialog):
    def reload_requests(self):
        pass


class RequestWidget(QWidget):
    """好友请求条目控件"""

    def __init__(
        self,
        token,
        username,
        content,
        request_id=None,
        state=None,
        parent: FriendRequestManageDialog_ = None,
    ):
        super().__init__()
        self.token = token
        self.username = username
        self.content = content
        self.request_id = request_id
        self.parent = parent
        friend_request_widget.Ui_Form().setupUi(self)

        # 设置显示内容
        self.findChild(QFrame, "frame_3").findChild(QLabel, "label").setText(username)
        self.findChild(QFrame, "frame_3").findChild(QLabel, "label_2").setText(content)

        if request_id:
            self.accept_button = self.findChild(QToolButton, "toolButton")
            self.reject_button = self.findChild(QToolButton, "toolButton_2")
            self.accept_button.clicked.connect(self.accept_request)
            self.reject_button.clicked.connect(self.reject_request)
        else:
            # 已处理请求（仅展示状态）
            self.accept_button = self.findChild(QToolButton, "toolButton")
            self.accept_button.setEnabled(False)
            self.accept_button.setText(state)
            self.findChild(QToolButton, "toolButton_2").setEnabled(False)
            self.findChild(QToolButton, "toolButton_2").hide()

    def accept_request(self):
        response = accept_friend_request(self.token, self.request_id)
        if response.status_code == 200:
            task.append("reload_friends_list")
            self.parent.reload_requests()
        else:
            show_api_error(self, "接受好友请求", response)

    def reject_request(self):
        response = reject_friend_request(self.token, self.request_id)
        if response.status_code == 200:
            task.append("reload_friends_list")
            self.parent.reload_requests()
        else:
            show_api_error(self, "拒绝好友请求", response)


class FriendRequestManageDialog(FriendRequestManageDialog_):
    """好友请求管理窗口"""

    def __init__(self, token):
        super().__init__()
        self.token = token
        request_manage.Ui_Dialog().setupUi(self)

        self.scroll_area = self.findChild(QScrollArea, "scrollArea")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)

        self.reload_requests()

    def reload_requests(self):
        """重新加载并显示所有请求"""
        incoming_resp = get_incoming_requests(self.token)
        outgoing_resp = get_outgoing_requests(self.token)

        # 检查请求是否成功
        if incoming_resp.status_code != 200:
            show_api_error(self, "获取收到的请求", incoming_resp)
            return
        if outgoing_resp.status_code != 200:
            show_api_error(self, "获取发出的请求", outgoing_resp)
            return

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 收到的请求
        layout.addWidget(QLabel("你收到的请求"))
        for req in incoming_resp.json()["requests"]:
            layout.addWidget(
                RequestWidget(
                    self.token,
                    req["from_username"],
                    req["message"],
                    req["request_id"],
                    parent=self,
                )
            )

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # 发出的请求
        layout.addWidget(QLabel("你发出的请求"))
        for req in outgoing_resp.json()["requests"]:
            status_map = {
                "pending": "等待处理中",
                "accepted": "对方已通过",
                "rejected": "对方已拒绝",
            }
            state = status_map.get(req["status"], req["status"])
            layout.addWidget(
                RequestWidget(
                    self.token, req["to_username"], req["message"], state=state
                )
            )

        self.scroll_area.setWidget(content_widget)


class SearchUsersDialog(QDialog):
    """搜索用户窗口"""

    def __init__(self, token):
        super().__init__()
        self.token = token
        search_users_ui.Ui_Dialog().setupUi(self)

        # 搜索相关控件
        frame2 = self.findChild(QFrame, "frame_2")
        self.search_button = frame2.findChild(QToolButton, "toolButton")
        self.search_button.clicked.connect(self.search_users)

        self.search_edit = frame2.findChild(QLineEdit, "lineEdit")
        self.list_view = self.findChild(QListView, "listView")
        self.list_view.doubleClicked.connect(self.add_friend)

        # 请求管理按钮
        self.request_manage_button = frame2.findChild(QToolButton, "toolButton_2")
        self.request_manage_button.clicked.connect(self.open_request_manage)

    def open_request_manage(self):
        FriendRequestManageDialog(self.token).exec()

    def add_friend(self):
        selected_username = self.list_view.model().data(self.list_view.currentIndex())
        dialog = AddFriendDialog(self.token, selected_username)
        dialog.exec()

    def search_users(self):
        query = self.search_edit.text()
        response = search_users(self.token, query)
        self.list_view.setModel(QStringListModel([]))
        if response.status_code == 200:
            users = response.json()["users"]
            self.list_view.setModel(QStringListModel(users))
        else:
            show_api_error(self, "搜索用户", response)


class LoginWindow(RegLogWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("login.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        self.login_button = self.window.findChild(QPushButton, "login")
        self.login_button.clicked.connect(self.do_login)

        self.register_link = self.window.findChild(QCommandLinkButton, "register_2")
        self.register_link.clicked.connect(self.go_register)

        self.username_edit = self.window.findChild(QLineEdit, "user_name")
        self.password_edit = self.window.findChild(QLineEdit, "password")

    def do_login(self):
        response = login(self.username_edit.text(), self.password_edit.text())
        if response.status_code == 200:
            QMessageBox.information(self, "登录", "登录成功!")
            self.logged_in = True
            self.action = ""
            self.user_name = self.username_edit.text()
            self.password = self.password_edit.text()
            self.token = response.json().get("token")
            self.window.close()
        else:
            show_api_error(self, "登录", response)

    def go_register(self):
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
        self.register_button.clicked.connect(self.do_register)

        self.login_link = self.window.findChild(QCommandLinkButton, "login")
        self.login_link.clicked.connect(self.go_login)

        self.username_edit = self.window.findChild(QLineEdit, "user_name")
        self.password_edit = self.window.findChild(QLineEdit, "password")
        self.confirm_edit = self.window.findChild(QLineEdit, "password_2")

    def do_register(self):
        if self.password_edit.text() != self.confirm_edit.text():
            QMessageBox.warning(self, "注册", "两次输入的密码不一致")
            return

        response = register(self.username_edit.text(), self.password_edit.text())
        if response.status_code == 201:
            QMessageBox.information(self, "注册", "注册成功！请登录！")
            self.go_login()
        else:
            show_api_error(self, "注册", response)

    def go_login(self):
        self.action = "login"
        self.window.close()


class AddFriendDialog(QDialog):
    """发送好友请求对话框"""

    def __init__(self, token, friend_username):
        super().__init__()
        self.token = token
        self.friend_username = friend_username
        add_friend.Ui_Dialog().setupUi(self)

        # 提示标签
        label = self.findChild(QFrame, "frame").findChild(QLabel, "label")
        label.setText(f"添加好友: {friend_username}。请填写验证信息。")

        # 按钮
        frame2 = self.findChild(QFrame, "frame_2")
        self.ok_button = frame2.findChild(QPushButton, "pushButton")
        self.cancel_button = frame2.findChild(QPushButton, "pushButton_2")

        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.send_request)

        # 验证信息输入框
        self.message_edit = self.findChild(QFrame, "frame").findChild(
            QPlainTextEdit, "plainTextEdit"
        )

    def send_request(self):
        message = self.message_edit.toPlainText()
        response = send_friend_request(self.token, self.friend_username, message)
        if response.status_code == 201:
            QMessageBox.information(self, "添加好友", "好友请求已发送!")
            self.close()
        else:
            show_api_error(self, "添加好友", response)


class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self):
        super().__init__()
        settings.Ui_Dialog().setupUi(self)

        # 主题相关控件
        self.light_theme_radio = self.findChild(QRadioButton, "light_theme_radio")
        self.dark_theme_radio = self.findChild(QRadioButton, "dark_theme_radio")

        # 字体相关控件
        self.font_family_combo = self.findChild(QComboBox, "font_family_combo")
        self.font_size_spin = self.findChild(QSpinBox, "font_size_spin")
        self.apply_font_button = self.findChild(QPushButton, "apply_font_button")
        self.select_font_file_button = self.findChild(QPushButton, "select_font_file_button")

        # 关于标签页控件
        self.credits_text_browser = self.findChild(QTextBrowser, "credits_text_browser")

        # 先加载可用字体
        self.load_fonts()

        # 再加载保存的设置
        self.load_settings()

        # 加载致谢内容
        self.load_credits()

        # 连接信号
        self.light_theme_radio.toggled.connect(self.on_theme_changed)
        self.dark_theme_radio.toggled.connect(self.on_theme_changed)
        self.apply_font_button.clicked.connect(self.apply_font)
        self.select_font_file_button.clicked.connect(self.select_font_file)

    def load_settings(self):
        """从配置文件加载设置"""
        # 加载主题设置
        theme = get_setting("theme", "light")
        if theme == "dark":
            self.dark_theme_radio.setChecked(True)
        else:
            self.light_theme_radio.setChecked(True)

        # 加载字体设置
        font_family = get_setting("font.family", "")
        font_size = get_setting("font.size", 12)

        if font_family:
            index = self.font_family_combo.findText(font_family)
            if index >= 0:
                self.font_family_combo.setCurrentIndex(index)

        self.font_size_spin.setValue(font_size)

    def load_fonts(self):
        """加载系统可用字体"""
        font_families = QFontDatabase.families()
        self.font_family_combo.addItems(font_families)

    def select_font_file(self):
        """选择本地TTF字体文件"""
        font_file, _ = QFileDialog.getOpenFileName(
            self,
            "选择字体文件",
            "",
            "字体文件 (*.ttf *.otf *.TTF *.OTF);;所有文件 (*)"
        )
        
        if font_file:
            # 加载字体文件
            font_id = QFontDatabase.addApplicationFont(font_file)
            if font_id == -1:
                QMessageBox.warning(self, "错误", "无法加载字体文件")
                return
            
            # 获取字体族名称
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                
                # 检查是否已在列表中
                index = self.font_family_combo.findText(font_family)
                if index < 0:
                    # 添加到列表
                    self.font_family_combo.addItem(font_family)
                    index = self.font_family_combo.count() - 1
                
                # 选中该字体
                self.font_family_combo.setCurrentIndex(index)
                
                # 保存字体文件路径
                set_setting("font.file_path", font_file)
                
                QMessageBox.information(self, "成功", f"已加载字体：{font_family}")

    def load_credits(self):
        """加载并显示 CREDITS.md 内容"""
        credits_file = "CREDITS.md"
        if not os.path.exists(credits_file):
            self.credits_text_browser.setMarkdown("# 致谢\n\n未找到 CREDITS.md 文件")
            return

        try:
            with open(credits_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.credits_text_browser.setMarkdown(content)
        except Exception as e:
            self.credits_text_browser.setMarkdown(f"# 致谢\n\n加载失败：{str(e)}")

    def on_theme_changed(self):
        """主题切换处理"""
        if self.dark_theme_radio.isChecked():
            self.apply_theme("dark")
            set_setting("theme", "dark")
        else:
            self.apply_theme("light")
            set_setting("theme", "light")

    def apply_theme(self, theme):
        """应用主题"""
        app = QApplication.instance()
        if not app:
            return

        palette = QPalette()

        if theme == "dark":
            # 深色主题
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # 浅色主题（默认）
            palette = QPalette()

        app.setPalette(palette)

    def apply_font(self):
        """应用字体设置"""
        font_family = self.font_family_combo.currentText()
        font_size = self.font_size_spin.value()

        app = QApplication.instance()
        if app:
            app.setFont(QFont(font_family, font_size))

        # 保存设置
        set_setting("font.family", font_family)
        set_setting("font.size", font_size)


class ChattingMainWindow(QMainWindow):
    def __init__(self, password, user_name, token):
        super().__init__()
        self.password = password
        self.user_name = user_name
        self.token = token
        self.state = ""  # 用于标记退出方式

        loader = QUiLoader()
        ui_file = QFile("chatting_main.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        # 好友列表
        dock = self.window.findChild(QDockWidget, "dockWidget_4")
        contents = dock.findChild(QWidget, "dockWidgetContents_5")
        self.friends_list_view = contents.findChild(QListView, "friends_list")
        self.friends_list_view.doubleClicked.connect(self.show_friend_info)

        # 添加好友按钮
        frame2 = contents.findChild(QFrame, "frame_2")
        self.add_friend_button = frame2.findChild(QToolButton, "add_friends")
        self.add_friend_button.clicked.connect(self.open_search_users)

        # 登出按钮
        frame = contents.findChild(QFrame, "frame")
        self.logout_button = frame.findChild(QToolButton, "toolButton_3")
        self.logout_button.clicked.connect(self.do_logout)

        # 设置按钮
        self.settings_button = frame.findChild(QToolButton, "toolButton_2")
        self.settings_button.clicked.connect(self.open_settings)

        # 定时处理全局任务
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_tasks)
        self.timer.start(200)  # 200ms

        # 初始加载好友列表
        self.reload_friends_list()

    def process_tasks(self):
        """在主线程中处理任务队列"""
        # 复制任务列表，避免迭代时修改原列表
        for t in task[:]:
            if t == "reload_friends_list":
                self.reload_friends_list()
                task.remove(t)
            elif t == "reload_request_list":
                # 请求列表窗口如果打开，需要刷新；此处仅作标记，实际刷新由窗口自身处理
                task.remove(t)

    def open_search_users(self):
        dialog = SearchUsersDialog(self.token)
        dialog.exec()

    def open_settings(self):
        dialog = SettingsDialog()
        dialog.exec()

    def reload_friends_list(self):
        """刷新好友列表，返回最新数据"""
        response = get_friends_list(self.token)
        if response.status_code == 200:
            data = response.json()
            self.friends_list_data = data  # 保存供详情使用
            usernames = [f["username"] for f in data.get("friends", [])]
            usernames.sort()
            model = QStringListModel()
            model.setStringList(usernames)
            self.friends_list_view.setModel(model)
        else:
            show_api_error(self, "获取好友列表", response)
        return self.friends_list_data

    def show_friend_info(self):
        """双击好友显示详细信息"""
        index = self.friends_list_view.currentIndex().row()
        friend = self.friends_list_data.get("friends", [])[index]
        info = (
            f"用户名: {friend.get('username')}\n"
            f"用户ID: {friend.get('user_id')}\n"
            f"添加时间: {friend.get('created_at')}"
        )
        QMessageBox.information(self, "好友信息", info)

    def do_logout(self):
        response = logout(self.token)
        if response.status_code == 200:
            self.state = "logout"
            self.window.close()
        else:
            show_api_error(self, "登出", response)


def restart_application():
    """重启应用程序：关闭所有窗口并重新启动程序"""
    import subprocess
    import sys

    # 关闭所有窗口
    app = QApplication.instance()
    if app:
        app.closeAllWindows()

    # 重新启动程序
    python = sys.executable
    os.execv(python, [python] + sys.argv)


def run_auth_flow():
    """运行登录/注册认证流程"""
    app = QApplication.instance() or QApplication(sys.argv)
    app.setWindowIcon(QIcon("ico/ico.png"))

    # 加载并应用主题设置
    theme = get_setting("theme", "light")
    if theme == "dark":
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

    # 加载并应用字体设置
    font_family = get_setting("font.family", "")
    font_size = get_setting("font.size", 12)
    font_file_path = get_setting("font.file_path", "")

    # 先尝试加载用户自定义的字体文件
    if font_file_path and os.path.exists(font_file_path):
        custom_font_id = QFontDatabase.addApplicationFont(font_file_path)
        if custom_font_id != -1:
            custom_font_families = QFontDatabase.applicationFontFamilies(custom_font_id)
            if custom_font_families:
                print(f"成功加载自定义字体: {custom_font_families[0]}")

    # 加载默认字体作为后备
    font_relative = r"font/SourceHan/Variable/TTF/SourceHanSansSC-VF.ttf"
    font_path = os.path.abspath(font_relative)
    if not os.path.exists(font_path):
        print(f"字体文件不存在: {font_path}")
        return

    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"字体加载失败: {font_path}")
    else:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            default_font_family = font_families[0]
            print(f"成功加载字体族: {default_font_family}")
            if font_family:
                app.setFont(QFont(font_family, font_size))
            else:
                app.setFont(QFont(default_font_family, 12))
        else:
            print("字体加载成功但未返回任何字体族")

    # 初始进入登录
    current = LoginWindow()
    current.window.show()
    app.exec()

    while True:
        if current.logged_in:
            # 登录成功，进入主窗口
            main_win = ChattingMainWindow(
                current.password, current.user_name, current.token
            )
            main_win.window.show()
            app.exec()
            if main_win.state == "logout":
                # 登出后重新认证
                current = LoginWindow()
                current.window.show()
                app.exec()
            else:
                # 直接关闭主窗口，退出程序
                break
        elif hasattr(current, "action") and current.action:
            # 切换到登录或注册
            if current.action == "register":
                current = RegisterWindow()
            elif current.action == "login":
                current = LoginWindow()
            current.window.show()
            app.exec()
        else:
            # 窗口被直接关闭，退出程序
            break

    app.quit()


if __name__ == "__main__":
    run_auth_flow()
