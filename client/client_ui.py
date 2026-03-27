"""
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
"""

import json
import os
import sys
from datetime import datetime
from http import HTTPStatus

import add_friend
import friend_request_widget
import request_manage
import search_users_ui
import settings
from client_api import (accept_friend_request, check_server_version,
                        delete_message, get_friends_list,
                        get_incoming_requests, get_messages,
                        get_outgoing_requests, get_setting, get_user_info,
                        login, logout, register, reject_friend_request,
                        search_users, send_friend_request, send_message,
                        set_setting, update_user_profile)
from PySide6.QtCore import QFile, QPointF, QSize, QStringListModel, Qt, QTimer
from PySide6.QtGui import (QColor, QFont, QFontDatabase, QIcon,
                           QPainter, QPalette, QPixmap, QStandardItem,
                           QStandardItemModel)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QComboBox, QCommandLinkButton,
                               QDialog, QDockWidget, QFileDialog, QFrame,
                               QHBoxLayout, QLabel, QLineEdit, QListView,
                               QListWidget, QListWidgetItem, QMainWindow,
                               QMessageBox, QPlainTextEdit, QPushButton,
                               QRadioButton, QScrollArea, QSpinBox,
                               QTabWidget, QTextBrowser, QTextEdit,
                               QToolButton, QVBoxLayout, QWidget)

# 全局任务队列（所有操作在主线程处理，故无需锁）
task = []

version = get_setting("version")


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
        parent: FriendRequestManageDialog_ | None = None,
    ):
        super().__init__()
        self.token = token
        self.username = username
        self.content = content
        self.request_id = request_id
        self._parent = parent
        friend_request_widget.Ui_Form().setupUi(self)

        # 设置显示内容
        frame_3 = self.findChild(QFrame, "frame_3")
        if frame_3:
            label = frame_3.findChild(QLabel, "label")
            if label:
                label.setText(username)
            label_2 = frame_3.findChild(QLabel, "label_2")
            if label_2:
                label_2.setText(content)

        if request_id:
            self.accept_button = self.findChild(QToolButton, "toolButton")
            self.reject_button = self.findChild(QToolButton, "toolButton_2")
            if self.accept_button:
                self.accept_button.clicked.connect(self.accept_request)
            if self.reject_button:
                self.reject_button.clicked.connect(self.reject_request)
        else:
            # 已处理请求（仅展示状态）
            self.accept_button = self.findChild(QToolButton, "toolButton")
            if self.accept_button:
                self.accept_button.setEnabled(False)
                self.accept_button.setText(state)
            tool_button_2 = self.findChild(QToolButton, "toolButton_2")
            if tool_button_2:
                tool_button_2.setEnabled(False)
                tool_button_2.hide()

    def accept_request(self):
        response = accept_friend_request(self.token, self.request_id)
        if response.status_code == HTTPStatus.OK:
            task.append("reload_friends_list")
            if self._parent:
                self._parent.reload_requests()
        else:
            show_api_error(self, "接受好友请求", response)

    def reject_request(self):
        response = reject_friend_request(self.token, self.request_id)
        if response.status_code == HTTPStatus.OK:
            task.append("reload_friends_list")
            if self._parent:
                self._parent.reload_requests()
        else:
            show_api_error(self, "拒绝好友请求", response)


class FriendRequestManageDialog(FriendRequestManageDialog_):
    """好友请求管理窗口"""

    def __init__(self, token):
        super().__init__()
        self.token = token
        request_manage.Ui_Dialog().setupUi(self)

        if (scroll_area := self.findChild(QScrollArea, "scrollArea")) is None:
            raise RuntimeError
        else:
            self.scroll_area = scroll_area

        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)

        self.reload_requests()

    def reload_requests(self):
        """重新加载并显示所有请求"""
        incoming_resp = get_incoming_requests(self.token)
        outgoing_resp = get_outgoing_requests(self.token)

        # 检查请求是否成功
        if incoming_resp.status_code != HTTPStatus.OK:
            show_api_error(self, "获取收到的请求", incoming_resp)
            return
        if outgoing_resp.status_code != HTTPStatus.OK:
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
        if response.status_code == HTTPStatus.OK:
            users = response.json()["users"]
            self.list_view.setModel(QStringListModel(users))
        else:
            show_api_error(self, "搜索用户", response)


class LoginWindow(RegLogWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("ChattingClientFile/ui/login.ui")
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
        if response.status_code == HTTPStatus.OK:
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
        ui_file = QFile("ChattingClientFile/ui/register.ui")
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
        if response.status_code == HTTPStatus.CREATED:
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
        if response.status_code == HTTPStatus.CREATED:
            QMessageBox.information(self, "添加好友", "好友请求已发送!")
            self.close()
        else:
            show_api_error(self, "添加好友", response)


class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, user_name=None, token=None):
        super().__init__()
        settings.Ui_Dialog().setupUi(self)
        self.user_name = user_name
        self.token = token

        # 主题相关控件
        self.light_theme_radio = self.findChild(QRadioButton, "light_theme_radio")
        self.dark_theme_radio = self.findChild(QRadioButton, "dark_theme_radio")

        # 字体相关控件
        self.font_family_combo = self.findChild(QComboBox, "font_family_combo")
        self.font_size_spin = self.findChild(QSpinBox, "font_size_spin")
        self.apply_font_button = self.findChild(QPushButton, "apply_font_button")
        self.select_font_file_button = self.findChild(
            QPushButton, "select_font_file_button"
        )

        # 网络相关控件
        self.public_key_edit = self.findChild(QLineEdit, "public_key_edit")
        self.select_public_key_button = self.findChild(
            QPushButton, "select_public_key_button"
        )
        self.server_url_edit = self.findChild(QLineEdit, "server_url_edit")
        self.update_server_edit = self.findChild(QLineEdit, "update_server_edit")
        self.check_server_version_button = self.findChild(
            QPushButton, "check_server_version_button"
        )
        self.check_client_version_button = self.findChild(
            QPushButton, "check_client_version_button"
        )
        self.update_client_button = self.findChild(QPushButton, "update_client_button")
        self.ok_button = self.findChild(QPushButton, "ok_button")
        self.cancel_button = self.findChild(QPushButton, "cancel_button")

        # 关于标签页控件
        self.credits_text_browser = self.findChild(QTextBrowser, "credits_text_browser")

        # 个人资料标签页
        self.tabWidget = self.findChild(QTabWidget, "tabWidget")
        self.add_profile_tab()

        # 先加载可用字体
        self.load_fonts()

        # 再加载保存的设置
        self.load_settings()

        # 加载个人资料
        if self.user_name and self.token:
            self.load_profile()

        # 加载致谢内容
        self.load_credits()

        # 连接信号
        self.light_theme_radio.toggled.connect(self.on_theme_changed)
        self.dark_theme_radio.toggled.connect(self.on_theme_changed)
        self.apply_font_button.clicked.connect(self.apply_font)
        self.select_font_file_button.clicked.connect(self.select_font_file)
        self.select_public_key_button.clicked.connect(self.select_public_key)
        self.check_server_version_button.clicked.connect(self.check_server_version)
        self.check_client_version_button.clicked.connect(self.check_client_version)
        self.ok_button.clicked.connect(self.apply_net_settings)
        if hasattr(self, "save_profile_button"):
            self.save_profile_button.clicked.connect(self.save_profile)

    def add_profile_tab(self):
        """添加个人资料标签页"""
        profile_tab = QWidget()
        self.tabWidget.addTab(profile_tab, "个人资料")

        layout = QVBoxLayout(profile_tab)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 个人资料表单
        profile_frame = QFrame()
        profile_layout = QVBoxLayout(profile_frame)

        # 头像
        avatar_layout = QHBoxLayout()
        avatar_label = QLabel("头像：")
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(80, 80)
        self.avatar_label.setStyleSheet(
            "border-radius: 40px; background-color: #E0E0E0;"
        )
        avatar_button = QPushButton("选择头像")
        avatar_button.clicked.connect(self.select_avatar)
        avatar_layout.addWidget(avatar_label)
        avatar_layout.addWidget(avatar_button)
        avatar_layout.addStretch()
        profile_layout.addLayout(avatar_layout)

        # 昵称
        nickname_layout = QHBoxLayout()
        nickname_label = QLabel("昵称：")
        self.nickname_edit = QLineEdit()
        nickname_layout.addWidget(nickname_label)
        nickname_layout.addWidget(self.nickname_edit)
        profile_layout.addLayout(nickname_layout)

        # 出生日期
        birthday_layout = QHBoxLayout()
        birthday_label = QLabel("出生日期：")
        self.birthday_edit = QLineEdit()
        self.birthday_edit.setPlaceholderText("YYYY-MM-DD")
        birthday_layout.addWidget(birthday_label)
        birthday_layout.addWidget(self.birthday_edit)
        profile_layout.addLayout(birthday_layout)

        # 性别
        gender_layout = QHBoxLayout()
        gender_label = QLabel("性别：")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "男", "女", "其他"])
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combo)
        profile_layout.addLayout(gender_layout)

        # 个人简介
        bio_layout = QVBoxLayout()
        bio_label = QLabel("个人简介：")
        self.bio_edit = QTextEdit()
        self.bio_edit.setFixedHeight(80)
        bio_layout.addWidget(bio_label)
        bio_layout.addWidget(self.bio_edit)
        profile_layout.addLayout(bio_layout)

        # 保存按钮
        self.save_profile_button = QPushButton("保存个人资料")
        profile_layout.addWidget(self.save_profile_button)

        # 头像数据
        self.avatar_data = None

        scroll_layout.addWidget(profile_frame)
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

    def select_avatar(self):
        """选择头像"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择头像", "", "图片文件 (*.jpg *.jpeg *.png *.bmp);;所有文件 (*)"
        )
        if file_path:
            # 显示预览
            from PySide6.QtGui import QPixmap

            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # 缩放头像
                scaled_pixmap = pixmap.scaled(
                    80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.avatar_label.setPixmap(scaled_pixmap)
                # 读取并编码头像数据
                import base64

                with open(file_path, "rb") as f:
                    avatar_bytes = f.read()
                    self.avatar_data = base64.b64encode(avatar_bytes).decode("utf-8")

    def load_profile(self):
        """加载个人资料"""
        response = get_user_info(self.token, self.user_name)
        if response.status_code == HTTPStatus.OK:
            user_info = response.json()
            self.nickname_edit.setText(user_info.get("nickname", ""))
            self.birthday_edit.setText(user_info.get("birthday", ""))
            gender = user_info.get("gender", "")
            gender_map = {"male": "男", "female": "女", "other": "其他"}
            gender_text = gender_map.get(gender, "")
            index = self.gender_combo.findText(gender_text)
            if index >= 0:
                self.gender_combo.setCurrentIndex(index)
            self.bio_edit.setText(user_info.get("bio", ""))
            # 加载头像
            avatar_data = user_info.get("avatar")
            if avatar_data:
                import base64

                from PySide6.QtGui import QImage, QPixmap

                try:
                    avatar_bytes = base64.b64decode(avatar_data)
                    image = QImage.fromData(avatar_bytes)
                    pixmap = QPixmap.fromImage(image)
                    scaled_pixmap = pixmap.scaled(
                        80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    self.avatar_label.setPixmap(scaled_pixmap)
                    self.avatar_data = avatar_data
                except Exception:
                    pass

    def save_profile(self):
        """保存个人资料"""
        nickname = self.nickname_edit.text().strip()
        birthday = self.birthday_edit.text().strip()
        gender_text = self.gender_combo.currentText()
        gender_map = {"男": "male", "女": "female", "其他": "other"}
        gender = gender_map.get(gender_text, "")
        bio = self.bio_edit.toPlainText().strip()

        response = update_user_profile(
            self.token,
            self.user_name,
            nickname=nickname,
            birthday=birthday,
            gender=gender,
            bio=bio,
            avatar=self.avatar_data,
        )

        if response.status_code == HTTPStatus.OK:
            QMessageBox.information(self, "成功", "个人资料更新成功")
        else:
            show_api_error(self, "更新个人资料", response)

    def apply_net_settings(self):
        reply = QMessageBox.warning(
            None,
            "警告",
            "如果贸然修改此设置可能会导致无法登录，以至于无法重新设置，除非手动修改 settings 文件。你确定要修改么？",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            set_setting("network.public_key_path", self.public_key_edit.text())
            set_setting("network.server_url", self.server_url_edit.text())
            set_setting("network.update_server_url", self.update_server_edit.text())
        else:
            print("用户选择了否。")

    def cancel_net_settings(self):
        # 加载网络设置
        if get_setting("network.public_key_path", "") == "":
            set_setting(
                "network.public_key_path", os.path.abspath("PUBLIC_KEY.chatting")
            )
        self.public_key_edit.setText(get_setting("network.public_key_path", ""))
        self.server_url_edit.setText(
            get_setting("network.server_url", "http://127.0.0.1:5000/api/v1")
        )
        self.update_server_edit.setText(
            get_setting("network.update_server_url", "http://127.0.0.1:5000/update")
        )

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

        # 加载网络设置
        if get_setting("network.public_key_path", "") == "":
            set_setting(
                "network.public_key_path", os.path.abspath("PUBLIC_KEY.chatting")
            )
        public_key_path = get_setting("network.public_key_path", "")
        server_url = get_setting("network.server_url", "http://127.0.0.1:5000/api/v1")
        update_server_url = get_setting(
            "network.update_server_url", "http://127.0.0.1:5000/update"
        )

        self.public_key_edit.setText(public_key_path)
        self.server_url_edit.setText(server_url)
        self.update_server_edit.setText(update_server_url)

    def load_fonts(self):
        """加载系统可用字体"""
        font_families = QFontDatabase.families()
        self.font_family_combo.addItems(font_families)

    def select_font_file(self):
        """选择本地TTF字体文件"""
        font_file, _ = QFileDialog.getOpenFileName(
            self, "选择字体文件", "", "字体文件 (*.ttf *.otf *.TTF *.OTF);;所有文件 (*)"
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
        credits_file = "../CREDITS.md"
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

    def select_public_key(self):
        """选择公钥文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择公钥文件", "", "公钥文件 (*.chatting);;所有文件 (*.*)"
        )
        if file_path:
            self.public_key_edit.setText(file_path)

    def check_server_version(self):
        rep = check_server_version()
        if rep.status_code == HTTPStatus.OK:
            QMessageBox.information(
                self, "服务器版本", f"服务器版本: {rep.json().get('version')}"
            )

    def check_client_version(self):
        """检测客户端版本"""
        QMessageBox.information(self, "客户端版本", f"客户端版本: {version}")

    def accept(self):
        """确认按钮点击事件"""
        # 保存网络设置
        public_key_path = self.public_key_edit.text()
        server_url = self.server_url_edit.text()
        update_server_url = self.update_server_edit.text()

        print(
            f"保存网络设置: public_key_path={public_key_path}, server_url={server_url}, update_server_url={update_server_url}"
        )

        # 保存网络设置
        set_setting("network.public_key_path", public_key_path)
        set_setting("network.server_url", server_url)
        set_setting("network.update_server_url", update_server_url)

        # 保存其他设置
        set_setting("network.public_key_path", self.public_key_edit.text())
        set_setting("network.server_url", self.server_url_edit.text())
        set_setting("network.update_server_url", self.update_server_edit.text())
        print("设置保存完成")

        super().accept()


def generate_avatar(username, size=40):
    """基于用户名生成随机头像"""
    # 基于用户名生成种子
    seed = hash(username)
    # 创建QPixmap
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    # 创建QPainter
    painter = QPainter(pixmap)
    # 设置抗锯齿
    painter.setRenderHint(QPainter.Antialiasing)
    # 基于种子生成颜色
    r = (seed * 137) % 200 + 55
    g = (seed * 173) % 200 + 55
    b = (seed * 191) % 200 + 55
    color = QColor(r, g, b)
    # 绘制圆形背景
    painter.setBrush(color)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, size, size)
    # 绘制用户名的首字母
    painter.setPen(QColor(255, 255, 255))
    font = QFont()
    font.setPointSize(size // 2)
    font.setBold(True)
    painter.setFont(font)
    # 获取首字母
    initial = username[0].upper() if username else "?"
    # 计算文本位置
    rect = pixmap.rect()
    painter.drawText(rect, Qt.AlignCenter, initial)
    # 结束绘制
    painter.end()
    return pixmap


class MessageItem(QWidget):
    """消息项组件"""

    def __init__(self, is_self, username, nickname, content, timestamp, avatar=None):
        super().__init__()
        self.is_self = is_self
        self.username = username
        self.nickname = nickname or username
        self.content = content
        self.timestamp = timestamp
        self.avatar = avatar

        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        if not is_self:
            # 对方消息：头像 + 消息
            avatar_label = QLabel()
            avatar_label.setFixedSize(40, 40)
            # 显示头像
            if avatar:
                import base64

                from PySide6.QtGui import QImage, QPixmap

                try:
                    avatar_bytes = base64.b64decode(avatar)
                    image = QImage.fromData(avatar_bytes)
                    pixmap = QPixmap.fromImage(image)
                    scaled_pixmap = pixmap.scaled(
                        40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    avatar_label.setPixmap(scaled_pixmap)
                except Exception:
                    # 如果头像加载失败，生成随机头像
                    avatar_pixmap = generate_avatar(username)
                    avatar_label.setPixmap(avatar_pixmap)
            else:
                # 生成随机头像
                avatar_pixmap = generate_avatar(username)
                avatar_label.setPixmap(avatar_pixmap)
            avatar_label.setStyleSheet("border-radius: 20px;")
            layout.addWidget(avatar_label)

            message_widget = QWidget()
            message_layout = QVBoxLayout(message_widget)
            message_layout.setContentsMargins(10, 0, 0, 0)

            # 昵称和时间
            top_widget = QWidget()
            top_layout = QHBoxLayout(top_widget)
            top_layout.setContentsMargins(0, 0, 0, 0)
            # 昵称
            nickname_label = QLabel(self.nickname)
            nickname_label.setStyleSheet("font-size: 10px; color: #666;")
            top_layout.addWidget(nickname_label)
            # 时间
            time_label = QLabel(self.timestamp)
            time_label.setStyleSheet("font-size: 10px; color: #999;")
            top_layout.addWidget(time_label)
            top_layout.addStretch()
            message_layout.addWidget(top_widget)

            # 消息内容
            content_label = QLabel(self.content)
            content_label.setWordWrap(True)
            content_label.setMaximumWidth(300)
            content_label.setStyleSheet(
                "background-color: #F0F0F0; border-radius: 10px; padding: 10px;"
            )
            message_layout.addWidget(content_label)

            layout.addWidget(message_widget)
            layout.addStretch()
        else:
            # 自己消息：消息 + 头像
            layout.addStretch()

            message_widget = QWidget()
            message_layout = QVBoxLayout(message_widget)
            message_layout.setContentsMargins(0, 0, 10, 0)

            # 消息内容和时间
            content_time_widget = QWidget()
            content_time_layout = QVBoxLayout(content_time_widget)
            content_time_layout.setContentsMargins(0, 0, 0, 0)
            # 消息内容
            content_label = QLabel(self.content)
            content_label.setWordWrap(True)
            content_label.setMaximumWidth(300)
            content_label.setStyleSheet(
                "background-color: #DCF8C6; border-radius: 10px; padding: 10px;"
            )
            content_time_layout.addWidget(content_label)
            # 时间
            time_label = QLabel(self.timestamp)
            time_label.setStyleSheet("font-size: 10px; color: #999;")
            time_label.setAlignment(Qt.AlignRight)
            content_time_layout.addWidget(time_label)
            message_layout.addWidget(content_time_widget)

            layout.addWidget(message_widget)

            avatar_label = QLabel()
            avatar_label.setFixedSize(40, 40)
            # 显示头像
            if avatar:
                import base64

                from PySide6.QtGui import QImage, QPixmap

                try:
                    avatar_bytes = base64.b64decode(avatar)
                    image = QImage.fromData(avatar_bytes)
                    pixmap = QPixmap.fromImage(image)
                    scaled_pixmap = pixmap.scaled(
                        40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    avatar_label.setPixmap(scaled_pixmap)
                except Exception:
                    # 如果头像加载失败，生成随机头像
                    avatar_pixmap = generate_avatar(username)
                    avatar_label.setPixmap(avatar_pixmap)
            else:
                # 生成随机头像
                avatar_pixmap = generate_avatar(username)
                avatar_label.setPixmap(avatar_pixmap)
            avatar_label.setStyleSheet("border-radius: 20px;")
            layout.addWidget(avatar_label)


class ChattingMainWindow(QMainWindow):
    def __init__(self, password, user_name, token):
        super().__init__()
        self.password = password
        self.user_name = user_name
        self.token = token
        loader = QUiLoader()
        ui_file = QFile("ChattingClientFile/ui/chatting_main.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        # 好友列表
        dock = self.window.findChild(QDockWidget, "dockWidget_4")
        contents = dock.findChild(QWidget, "dockWidgetContents_5")
        # 获取布局
        layout = contents.layout()
        # 移除原来的QListView
        old_list_view = contents.findChild(QListView, "friends_list")
        if old_list_view:
            layout.removeWidget(old_list_view)
            old_list_view.deleteLater()
        # 创建新的QListWidget
        self.friends_list_widget = QListWidget()
        self.friends_list_widget.itemDoubleClicked.connect(self.open_chat)
        # 确保工具栏在好友列表下方
        # 先移除所有组件
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        # 重新添加组件
        # 添加搜索和添加好友按钮
        frame2 = QFrame()
        frame2_layout = QHBoxLayout(frame2)
        search_edit = QLineEdit()
        search_button = QToolButton()
        search_button.setText("搜索")
        add_friend_button = QToolButton()
        add_friend_button.setText("+")
        add_friend_button.clicked.connect(self.open_search_users)
        frame2_layout.addWidget(search_edit)
        frame2_layout.addWidget(search_button)
        frame2_layout.addWidget(add_friend_button)
        layout.addWidget(frame2)
        # 添加好友列表
        layout.addWidget(self.friends_list_widget, 1)
        # 添加工具栏
        frame = QFrame()
        frame_layout = QHBoxLayout(frame)
        settings_button = QToolButton()
        settings_button.setText("设置")
        settings_button.clicked.connect(self.open_settings)
        logout_button = QToolButton()
        logout_button.setText("登出")
        logout_button.clicked.connect(self.do_logout)
        more_button = QToolButton()
        more_button.setText("...")
        frame_layout.addWidget(settings_button)
        frame_layout.addWidget(logout_button)
        frame_layout.addWidget(more_button)
        layout.addWidget(frame)

        # 工具栏按钮已经在上面重新创建并连接了信号

        # 聊天区域
        central_widget = self.window.findChild(QWidget, "centralwidget")
        # 移除现有的布局
        existing_layout = central_widget.layout()
        if existing_layout:
            QWidget().setLayout(existing_layout)  # 转移布局的所有权
        # 添加新的布局
        chat_layout = QVBoxLayout(central_widget)
        chat_layout.setContentsMargins(0, 0, 0, 0)

        # 聊天标题栏
        self.chat_title = QLabel("选择好友开始聊天")
        self.chat_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; padding: 10px;"
        )
        chat_layout.addWidget(self.chat_title)

        # 消息显示区域
        self.messages_scroll = QScrollArea()
        self.messages_scroll.setWidgetResizable(True)
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_layout.setSpacing(10)
        self.messages_scroll.setWidget(self.messages_widget)
        chat_layout.addWidget(self.messages_scroll, 1)

        # 输入区域
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(10, 10, 10, 10)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(80)
        self.message_input.setPlaceholderText("输入消息...")
        input_layout.addWidget(self.message_input, 1)

        self.send_button = QPushButton("发送")
        self.send_button.setFixedSize(80, 80)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        chat_layout.addWidget(input_widget)

        # 定时处理全局任务
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_tasks)
        self.timer.start(200)  # 200ms

        # 定时检查新消息
        self.message_timer = QTimer()
        self.message_timer.timeout.connect(self.check_new_messages)
        self.message_timer.start(5000)  # 5秒检查一次

        # 定时刷新好友列表（实时更新资料）
        self.friends_refresh_timer = QTimer()
        self.friends_refresh_timer.timeout.connect(self.reload_friends_list)
        self.friends_refresh_timer.start(10000)  # 10秒刷新一次

        # 当前聊天的好友
        self.current_friend = None

        # 本地消息存储
        self.local_messages = {}
        # 加载本地存储的消息
        self.load_local_messages()

        # 初始加载好友列表
        self.reload_friends_list()

        # 设置窗口最小大小
        self.window.setMinimumSize(800, 600)

        # 窗口关闭时保存消息
        self.window.closeEvent = self.on_close

    def get_messages_file(self):
        """获取消息存储文件路径"""
        return f"messages_{self.user_name}.json"

    def load_local_messages(self):
        """加载本地存储的消息"""
        messages_file = self.get_messages_file()
        if os.path.exists(messages_file):
            try:
                with open(messages_file, "r", encoding="utf-8") as f:
                    self.local_messages = json.load(f)
            except Exception as e:
                print(f"加载本地消息失败: {e}")
                self.local_messages = {}

    def save_local_messages(self):
        """保存消息到本地"""
        messages_file = self.get_messages_file()
        try:
            with open(messages_file, "w", encoding="utf-8") as f:
                json.dump(self.local_messages, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存本地消息失败: {e}")

    def on_close(self, event):
        """窗口关闭事件"""
        self.save_local_messages()
        event.accept()

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
        # 使用本地定义的 SettingsDialog 类
        dialog = SettingsDialog(self.user_name, self.token)
        dialog.exec()

    def reload_friends_list(self):
        """刷新好友列表，返回最新数据"""
        response = get_friends_list(self.token)
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            # Token无效，停止定时器并提示用户
            self.timer.stop()
            self.message_timer.stop()
            self.friends_refresh_timer.stop()
            QMessageBox.warning(self, "提示", "登录已过期，请重新登录")
            self.do_logout()
            return
        elif response.status_code == HTTPStatus.OK:
            data = response.json()
            self.friends_list_data = data  # 保存供详情使用
            friends = data.get("friends", [])
            # 清空列表
            self.friends_list_widget.clear()
            # 添加好友项
            for friend in friends:
                username = friend.get("username")
                # 获取最新的好友信息
                nickname = username
                try:
                    user_info = get_user_info(self.token, username)
                    if user_info.status_code == HTTPStatus.OK:
                        user_data = user_info.json()
                        nickname = user_data.get("nickname", username)
                except Exception:
                    pass
                # 创建好友项
                item = QListWidgetItem()
                item.setSizeHint(QSize(0, 60))  # 设置项高度
                # 创建好友项控件
                friend_widget = QWidget()
                friend_layout = QHBoxLayout(friend_widget)
                friend_layout.setContentsMargins(10, 5, 10, 5)
                # 头像
                avatar_label = QLabel()
                avatar_label.setFixedSize(40, 40)
                # 尝试获取好友头像
                has_avatar = False
                try:
                    # 获取好友信息
                    user_info = get_user_info(self.token, username)
                    if user_info.status_code == HTTPStatus.OK:
                        avatar_data = user_info.json().get("avatar")
                        if avatar_data:
                            import base64

                            from PySide6.QtGui import QImage, QPixmap

                            avatar_bytes = base64.b64decode(avatar_data)
                            image = QImage.fromData(avatar_bytes)
                            pixmap = QPixmap.fromImage(image)
                            scaled_pixmap = pixmap.scaled(
                                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
                            )
                            avatar_label.setPixmap(scaled_pixmap)
                            has_avatar = True
                except Exception:
                    pass
                # 如果没有头像，生成随机头像
                if not has_avatar:
                    avatar_pixmap = generate_avatar(username)
                    avatar_label.setPixmap(avatar_pixmap)
                avatar_label.setStyleSheet("border-radius: 20px;")
                friend_layout.addWidget(avatar_label)
                # 信息
                info_widget = QWidget()
                info_layout = QVBoxLayout(info_widget)
                info_layout.setContentsMargins(10, 0, 0, 0)
                # 昵称
                nickname_label = QLabel(nickname)
                nickname_label.setStyleSheet("font-weight: bold;")
                info_layout.addWidget(nickname_label)
                # 用户名
                username_label = QLabel(username)
                username_label.setStyleSheet("font-size: 10px; color: #666;")
                info_layout.addWidget(username_label)
                friend_layout.addWidget(info_widget)
                friend_layout.addStretch()
                # 设置项的控件
                self.friends_list_widget.addItem(item)
                self.friends_list_widget.setItemWidget(item, friend_widget)
        else:
            show_api_error(self, "获取好友列表", response)
        return self.friends_list_data

    def open_chat(self, item=None):
        """打开与好友的聊天窗口"""
        # 获取当前选中的好友
        current_item = item or self.friends_list_widget.currentItem()
        if not current_item:
            return
        # 获取好友索引
        index = self.friends_list_widget.row(current_item)
        friend = self.friends_list_data.get("friends", [])[index]
        self.current_friend = friend
        username = friend.get("username")

        # 获取最新的好友信息
        nickname = username
        try:
            user_info = get_user_info(self.token, username)
            if user_info.status_code == HTTPStatus.OK:
                user_data = user_info.json()
                nickname = user_data.get("nickname", username)
        except Exception:
            pass

        # 更新聊天标题
        self.chat_title.setText(f"与 {nickname} 聊天")

        # 清空消息显示
        for i in reversed(range(self.messages_layout.count())):
            widget = self.messages_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # 加载本地消息并更新头像
        if username in self.local_messages:
            for msg in self.local_messages[username]:
                self.add_message_item(msg)

    def send_message(self):
        """发送消息"""
        if not self.current_friend:
            QMessageBox.warning(self, "提示", "请先选择好友")
            return

        content = self.message_input.toPlainText().strip()
        if not content:
            return

        username = self.current_friend.get("username")

        # 获取自己的信息（包括头像）
        user_info = get_user_info(self.token, self.user_name)
        nickname = self.user_name
        avatar = None
        if user_info.status_code == HTTPStatus.OK:
            user_data = user_info.json()
            nickname = user_data.get("nickname", self.user_name)
            avatar = user_data.get("avatar")

        # 发送消息到服务器
        response = send_message(self.token, username, content)
        if response.status_code == HTTPStatus.CREATED:
            # 本地显示消息
            msg = {
                "is_self": True,
                "username": self.user_name,
                "nickname": nickname,
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "avatar": avatar,
            }
            self.add_message_item(msg)

            # 保存到本地
            if username not in self.local_messages:
                self.local_messages[username] = []
            self.local_messages[username].append(msg)
            # 保存到文件
            self.save_local_messages()

            # 清空输入框
            self.message_input.clear()
        else:
            show_api_error(self, "发送消息", response)

    def add_message_item(self, msg):
        """添加消息项"""
        # 获取最新的用户信息（包括头像）
        username = msg.get("username")
        nickname = msg.get("nickname")
        avatar = msg.get("avatar")

        # 尝试获取最新的用户信息
        try:
            user_info = get_user_info(self.token, username)
            if user_info.status_code == HTTPStatus.OK:
                user_data = user_info.json()
                nickname = user_data.get("nickname", username)
                avatar = user_data.get("avatar")
        except Exception:
            pass

        message_item = MessageItem(
            is_self=msg.get("is_self"),
            username=username,
            nickname=nickname,
            content=msg.get("content"),
            timestamp=msg.get("timestamp"),
            avatar=avatar,
        )
        self.messages_layout.addWidget(message_item)
        # 滚动到底部
        self.messages_scroll.verticalScrollBar().setValue(
            self.messages_scroll.verticalScrollBar().maximum()
        )

    def check_new_messages(self):
        """检查新消息"""
        response = get_messages(self.token)
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            # Token无效，停止定时器并提示用户
            self.timer.stop()
            self.message_timer.stop()
            self.friends_refresh_timer.stop()
            QMessageBox.warning(self, "提示", "登录已过期，请重新登录")
            self.do_logout()
            return
        elif response.status_code == HTTPStatus.OK:
            messages = response.json().get("messages", [])
            for msg in messages:
                from_username = msg.get("from_username")
                content = msg.get("content")
                created_at = msg.get("created_at")

                # 获取发送者信息
                user_info = get_user_info(self.token, from_username)
                nickname = from_username
                avatar = None
                if user_info.status_code == HTTPStatus.OK:
                    user_data = user_info.json()
                    nickname = user_data.get("nickname", from_username)
                    avatar = user_data.get("avatar")

                # 构建消息对象
                message = {
                    "is_self": False,
                    "username": from_username,
                    "nickname": nickname,
                    "content": content,
                    "timestamp": created_at,
                    "avatar": avatar,
                }

                # 保存到本地
                if from_username not in self.local_messages:
                    self.local_messages[from_username] = []
                self.local_messages[from_username].append(message)
                # 保存到文件
                self.save_local_messages()

                # 如果当前正在与该好友聊天，显示消息
                if (
                    self.current_friend
                    and self.current_friend.get("username") == from_username
                ):
                    self.add_message_item(message)

                # 从服务器删除消息
                delete_message(self.token, msg.get("id"))

    def do_logout(self):
        # 停止所有定时器
        self.timer.stop()
        self.message_timer.stop()
        self.friends_refresh_timer.stop()

        response = logout(self.token)
        if response.status_code == HTTPStatus.OK:
            self.state = "logout"
            self.window.close()
        else:
            show_api_error(self, "登出", response)


def restart_application():
    """重启应用程序：关闭所有窗口并重新启动程序"""
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
    app.setWindowIcon(QIcon("ChattingClientFile/ico/ico.png"))

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
    font_relative = (
        r"./ChattingClientFile/font/SourceHan/Variable/TTF/SourceHanSansSC-VF.ttf"
    )
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
            if hasattr(main_win, "state") and main_win.state == "logout":
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
    print(__doc__)
    run_auth_flow()
