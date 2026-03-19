import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTabWidget, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QGroupBox, QLabel, QSpinBox, QPushButton, QComboBox, QRadioButton, QLineEdit, QTextEdit, QCheckBox, QDateEdit, QMenuBar, QMenu, QStatusBar, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QFont, QAction

class VersioningUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("版本管理工具")
        self.setGeometry(0, 0, 800, 600)
        
        # 创建中央部件
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        # 创建主布局
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        
        # 创建标签页
        self.tabWidget = QTabWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.tabWidget)
        
        # 创建版本号管理标签页
        self.create_version_tab()
        
        # 创建分支命名标签页
        self.create_branch_tab()
        
        # 创建提交信息标签页
        self.create_commit_tab()
        
        # 创建 Changelog 生成标签页
        self.create_changelog_tab()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 初始化信号连接
        self.init_connections()
        
        # 初始化当前版本显示
        self.update_current_version()
        
        # 初始化分支名显示
        self.update_branch_name()
        
        # 初始化提交信息显示
        self.update_commit_message()
        
        # 初始化 Changelog 显示
        self.update_changelog()
        
        # 设置日期为当前日期
        self.dateEdit_changelog.setDate(datetime.now())
    
    def create_version_tab(self):
        self.tab_version = QWidget()
        self.tabWidget.addTab(self.tab_version, "版本号管理")
        
        self.verticalLayout_2 = QVBoxLayout(self.tab_version)
        
        # 版本号设置
        self.groupBox = QGroupBox("版本号设置")
        self.verticalLayout_2.addWidget(self.groupBox)
        
        self.gridLayout = QGridLayout(self.groupBox)
        
        # 主版本号
        self.label = QLabel("主版本号 (MAJOR):")
        self.gridLayout.addWidget(self.label, 0, 0)
        
        self.spinBox_major = QSpinBox()
        self.spinBox_major.setMinimum(0)
        self.spinBox_major.setValue(1)
        self.gridLayout.addWidget(self.spinBox_major, 0, 1)
        
        self.horizontalLayout_major = QHBoxLayout()
        self.gridLayout.addLayout(self.horizontalLayout_major, 0, 2)
        
        self.pushButton_major_up = QPushButton("↑")
        self.horizontalLayout_major.addWidget(self.pushButton_major_up)
        
        self.pushButton_major_down = QPushButton("↓")
        self.horizontalLayout_major.addWidget(self.pushButton_major_down)
        
        # 次版本号
        self.label_2 = QLabel("次版本号 (MINOR):")
        self.gridLayout.addWidget(self.label_2, 1, 0)
        
        self.spinBox_minor = QSpinBox()
        self.spinBox_minor.setMinimum(0)
        self.gridLayout.addWidget(self.spinBox_minor, 1, 1)
        
        self.horizontalLayout_minor = QHBoxLayout()
        self.gridLayout.addLayout(self.horizontalLayout_minor, 1, 2)
        
        self.pushButton_minor_up = QPushButton("↑")
        self.horizontalLayout_minor.addWidget(self.pushButton_minor_up)
        
        self.pushButton_minor_down = QPushButton("↓")
        self.horizontalLayout_minor.addWidget(self.pushButton_minor_down)
        
        # 修订号
        self.label_3 = QLabel("修订号 (PATCH):")
        self.gridLayout.addWidget(self.label_3, 2, 0)
        
        self.spinBox_patch = QSpinBox()
        self.spinBox_patch.setMinimum(0)
        self.gridLayout.addWidget(self.spinBox_patch, 2, 1)
        
        self.horizontalLayout_patch = QHBoxLayout()
        self.gridLayout.addLayout(self.horizontalLayout_patch, 2, 2)
        
        self.pushButton_patch_up = QPushButton("↑")
        self.horizontalLayout_patch.addWidget(self.pushButton_patch_up)
        
        self.pushButton_patch_down = QPushButton("↓")
        self.horizontalLayout_patch.addWidget(self.pushButton_patch_down)
        
        # 预发布版本
        self.label_4 = QLabel("预发布版本:")
        self.gridLayout.addWidget(self.label_4, 3, 0)
        
        self.comboBox_prerelease = QComboBox()
        self.comboBox_prerelease.addItems(["无", "alpha", "beta", "rc"])
        self.gridLayout.addWidget(self.comboBox_prerelease, 3, 1)
        
        self.spinBox_prerelease_version = QSpinBox()
        self.spinBox_prerelease_version.setMinimum(1)
        self.gridLayout.addWidget(self.spinBox_prerelease_version, 3, 2)
        
        # 当前版本
        self.groupBox_2 = QGroupBox("当前版本")
        self.verticalLayout_2.addWidget(self.groupBox_2)
        
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        
        self.label_current_version = QLabel("1.0.0")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_current_version.setFont(font)
        self.horizontalLayout.addWidget(self.label_current_version)
        
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        
        self.pushButton_copy_version = QPushButton("复制版本号")
        self.horizontalLayout.addWidget(self.pushButton_copy_version)
    
    def create_branch_tab(self):
        self.tab_branch = QWidget()
        self.tabWidget.addTab(self.tab_branch, "分支命名")
        
        self.verticalLayout_3 = QVBoxLayout(self.tab_branch)
        
        # 分支类型
        self.groupBox_3 = QGroupBox("分支类型")
        self.verticalLayout_3.addWidget(self.groupBox_3)
        
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        
        self.radioButton_feature = QRadioButton("功能分支 (feature)")
        self.radioButton_feature.setChecked(True)
        self.verticalLayout_4.addWidget(self.radioButton_feature)
        
        self.radioButton_bugfix = QRadioButton("错误修复分支 (bugfix)")
        self.verticalLayout_4.addWidget(self.radioButton_bugfix)
        
        self.radioButton_hotfix = QRadioButton("热修复分支 (hotfix)")
        self.verticalLayout_4.addWidget(self.radioButton_hotfix)
        
        self.radioButton_release = QRadioButton("发布分支 (release)")
        self.verticalLayout_4.addWidget(self.radioButton_release)
        
        # 分支描述
        self.groupBox_4 = QGroupBox("分支描述")
        self.verticalLayout_3.addWidget(self.groupBox_4)
        
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        
        self.lineEdit_branch_description = QLineEdit()
        self.lineEdit_branch_description.setPlaceholderText("输入分支描述，例如：user-login-api")
        self.verticalLayout_5.addWidget(self.lineEdit_branch_description)
        
        self.lineEdit_branch_version = QLineEdit()
        self.lineEdit_branch_version.setPlaceholderText("输入版本号，例如：v1.2.0")
        self.lineEdit_branch_version.setVisible(False)
        self.verticalLayout_5.addWidget(self.lineEdit_branch_version)
        
        # 生成的分支名
        self.groupBox_5 = QGroupBox("生成的分支名")
        self.verticalLayout_3.addWidget(self.groupBox_5)
        
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_5)
        
        self.label_branch_name = QLabel("feature/")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_branch_name.setFont(font)
        self.horizontalLayout_2.addWidget(self.label_branch_name)
        
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)
        
        self.pushButton_copy_branch = QPushButton("复制分支名")
        self.horizontalLayout_2.addWidget(self.pushButton_copy_branch)
    
    def create_commit_tab(self):
        self.tab_commit = QWidget()
        self.tabWidget.addTab(self.tab_commit, "提交信息")
        
        self.verticalLayout_6 = QVBoxLayout(self.tab_commit)
        
        # 提交类型
        self.groupBox_6 = QGroupBox("提交类型")
        self.verticalLayout_6.addWidget(self.groupBox_6)
        
        self.gridLayout_2 = QGridLayout(self.groupBox_6)
        
        self.comboBox_commit_type = QComboBox()
        self.comboBox_commit_type.addItems(["feat", "fix", "docs", "style", "refactor", "test", "chore"])
        self.gridLayout_2.addWidget(self.comboBox_commit_type, 0, 0)
        
        self.lineEdit_commit_scope = QLineEdit()
        self.lineEdit_commit_scope.setPlaceholderText("可选范围，例如：api")
        self.gridLayout_2.addWidget(self.lineEdit_commit_scope, 0, 1)
        
        self.checkBox_breaking = QCheckBox("破坏性变更")
        self.gridLayout_2.addWidget(self.checkBox_breaking, 0, 2)
        
        # 提交描述
        self.groupBox_7 = QGroupBox("提交描述")
        self.verticalLayout_6.addWidget(self.groupBox_7)
        
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_7)
        
        self.lineEdit_commit_description = QLineEdit()
        self.lineEdit_commit_description.setPlaceholderText("简短描述（不超过 50 字符）")
        self.verticalLayout_7.addWidget(self.lineEdit_commit_description)
        
        self.textEdit_commit_body = QTextEdit()
        self.textEdit_commit_body.setPlaceholderText("详细描述（可选）")
        self.verticalLayout_7.addWidget(self.textEdit_commit_body)
        
        self.lineEdit_commit_footer = QLineEdit()
        self.lineEdit_commit_footer.setPlaceholderText("脚注（可选，如 BREAKING CHANGE: 或 Closes #123）")
        self.verticalLayout_7.addWidget(self.lineEdit_commit_footer)
        
        # 生成的提交信息
        self.groupBox_8 = QGroupBox("生成的提交信息")
        self.verticalLayout_6.addWidget(self.groupBox_8)
        
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_8)
        
        self.textEdit_commit_message = QTextEdit()
        self.textEdit_commit_message.setReadOnly(True)
        font = QFont("Courier New")
        self.textEdit_commit_message.setFont(font)
        self.verticalLayout_8.addWidget(self.textEdit_commit_message)
        
        self.pushButton_copy_commit = QPushButton("复制提交信息")
        self.verticalLayout_8.addWidget(self.pushButton_copy_commit)
    
    def create_changelog_tab(self):
        self.tab_changelog = QWidget()
        self.tabWidget.addTab(self.tab_changelog, "Changelog 生成")
        
        self.verticalLayout_9 = QVBoxLayout(self.tab_changelog)
        
        # 版本信息
        self.groupBox_9 = QGroupBox("版本信息")
        self.verticalLayout_9.addWidget(self.groupBox_9)
        
        self.gridLayout_3 = QGridLayout(self.groupBox_9)
        
        self.label_5 = QLabel("版本号:")
        self.gridLayout_3.addWidget(self.label_5, 0, 0)
        
        self.lineEdit_changelog_version = QLineEdit()
        self.lineEdit_changelog_version.setText("1.0.0")
        self.gridLayout_3.addWidget(self.lineEdit_changelog_version, 0, 1)
        
        self.pushButton_use_current_version = QPushButton("使用当前版本")
        self.gridLayout_3.addWidget(self.pushButton_use_current_version, 0, 2)
        
        self.label_6 = QLabel("日期:")
        self.gridLayout_3.addWidget(self.label_6, 1, 0)
        
        self.dateEdit_changelog = QDateEdit()
        self.dateEdit_changelog.setCalendarPopup(True)
        self.gridLayout_3.addWidget(self.dateEdit_changelog, 1, 1)
        
        # 变更内容
        self.groupBox_10 = QGroupBox("变更内容")
        self.verticalLayout_9.addWidget(self.groupBox_10)
        
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_10)
        
        # Added
        self.groupBox_11 = QGroupBox("Added (新增)")
        self.verticalLayout_10.addWidget(self.groupBox_11)
        
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_11)
        
        self.textEdit_added = QTextEdit()
        self.textEdit_added.setPlaceholderText("每行一个新增功能")
        self.verticalLayout_11.addWidget(self.textEdit_added)
        
        # Changed
        self.groupBox_12 = QGroupBox("Changed (变更)")
        self.verticalLayout_10.addWidget(self.groupBox_12)
        
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_12)
        
        self.textEdit_changed = QTextEdit()
        self.textEdit_changed.setPlaceholderText("每行一个变更功能")
        self.verticalLayout_12.addWidget(self.textEdit_changed)
        
        # Fixed
        self.groupBox_13 = QGroupBox("Fixed (修复)")
        self.verticalLayout_10.addWidget(self.groupBox_13)
        
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_13)
        
        self.textEdit_fixed = QTextEdit()
        self.textEdit_fixed.setPlaceholderText("每行一个修复问题")
        self.verticalLayout_13.addWidget(self.textEdit_fixed)
        
        # Removed
        self.groupBox_14 = QGroupBox("Removed (移除)")
        self.verticalLayout_10.addWidget(self.groupBox_14)
        
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_14)
        
        self.textEdit_removed = QTextEdit()
        self.textEdit_removed.setPlaceholderText("每行一个移除功能")
        self.verticalLayout_14.addWidget(self.textEdit_removed)
        
        # 生成的 Changelog
        self.groupBox_15 = QGroupBox("生成的 Changelog")
        self.verticalLayout_9.addWidget(self.groupBox_15)
        
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_15)
        
        self.textEdit_changelog = QTextEdit()
        self.textEdit_changelog.setReadOnly(True)
        font = QFont("Courier New")
        self.textEdit_changelog.setFont(font)
        self.verticalLayout_15.addWidget(self.textEdit_changelog)
        
        self.horizontalLayout_3 = QHBoxLayout()
        self.verticalLayout_15.addLayout(self.horizontalLayout_3)
        
        self.pushButton_copy_changelog = QPushButton("复制 Changelog")
        self.horizontalLayout_3.addWidget(self.pushButton_copy_changelog)
        
        self.pushButton_save_changelog = QPushButton("保存到文件")
        self.horizontalLayout_3.addWidget(self.pushButton_save_changelog)
    
    def create_menu_bar(self):
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        
        self.menu = QMenu("文件", self)
        self.menubar.addMenu(self.menu)
        
        self.action_save_config = QAction("保存配置", self)
        self.menu.addAction(self.action_save_config)
        
        self.action_load_config = QAction("加载配置", self)
        self.menu.addAction(self.action_load_config)
        
        self.menu.addSeparator()
        
        self.action_exit = QAction("退出", self)
        self.menu.addAction(self.action_exit)
        
        self.menu_2 = QMenu("帮助", self)
        self.menubar.addMenu(self.menu_2)
        
        self.action_about = QAction("关于", self)
        self.menu_2.addAction(self.action_about)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
    
    def init_connections(self):
        # 版本号相关信号
        self.spinBox_major.valueChanged.connect(self.on_major_changed)
        self.spinBox_minor.valueChanged.connect(self.on_minor_changed)
        self.spinBox_patch.valueChanged.connect(self.update_current_version)
        self.comboBox_prerelease.currentIndexChanged.connect(self.update_current_version)
        self.spinBox_prerelease_version.valueChanged.connect(self.update_current_version)
        self.pushButton_major_up.clicked.connect(self.increment_major)
        self.pushButton_major_down.clicked.connect(self.decrement_major)
        self.pushButton_minor_up.clicked.connect(self.increment_minor)
        self.pushButton_minor_down.clicked.connect(self.decrement_minor)
        self.pushButton_patch_up.clicked.connect(self.increment_patch)
        self.pushButton_patch_down.clicked.connect(self.decrement_patch)
        self.pushButton_copy_version.clicked.connect(self.copy_version)
        
        # 分支相关信号
        self.radioButton_feature.toggled.connect(self.update_branch_name)
        self.radioButton_bugfix.toggled.connect(self.update_branch_name)
        self.radioButton_hotfix.toggled.connect(self.update_branch_name)
        self.radioButton_release.toggled.connect(self.update_branch_name)
        self.lineEdit_branch_description.textChanged.connect(self.update_branch_name)
        self.lineEdit_branch_version.textChanged.connect(self.update_branch_name)
        self.pushButton_copy_branch.clicked.connect(self.copy_branch)
        
        # 提交信息相关信号
        self.comboBox_commit_type.currentTextChanged.connect(self.update_commit_message)
        self.lineEdit_commit_scope.textChanged.connect(self.update_commit_message)
        self.checkBox_breaking.toggled.connect(self.update_commit_message)
        self.lineEdit_commit_description.textChanged.connect(self.update_commit_message)
        self.textEdit_commit_body.textChanged.connect(self.update_commit_message)
        self.lineEdit_commit_footer.textChanged.connect(self.update_commit_message)
        self.pushButton_copy_commit.clicked.connect(self.copy_commit)
        
        # Changelog 相关信号
        self.lineEdit_changelog_version.textChanged.connect(self.update_changelog)
        self.dateEdit_changelog.dateChanged.connect(self.update_changelog)
        self.textEdit_added.textChanged.connect(self.update_changelog)
        self.textEdit_changed.textChanged.connect(self.update_changelog)
        self.textEdit_fixed.textChanged.connect(self.update_changelog)
        self.textEdit_removed.textChanged.connect(self.update_changelog)
        self.pushButton_use_current_version.clicked.connect(self.use_current_version)
        self.pushButton_copy_changelog.clicked.connect(self.copy_changelog)
        self.pushButton_save_changelog.clicked.connect(self.save_changelog)
        
        # 菜单信号
        self.action_save_config.triggered.connect(self.save_config)
        self.action_load_config.triggered.connect(self.load_config)
        self.action_exit.triggered.connect(self.close)
        self.action_about.triggered.connect(self.show_about)
    
    def increment_major(self):
        self.spinBox_major.setValue(self.spinBox_major.value() + 1)
        
    def decrement_major(self):
        if self.spinBox_major.value() > 0:
            self.spinBox_major.setValue(self.spinBox_major.value() - 1)
        
    def increment_minor(self):
        self.spinBox_minor.setValue(self.spinBox_minor.value() + 1)
        
    def decrement_minor(self):
        if self.spinBox_minor.value() > 0:
            self.spinBox_minor.setValue(self.spinBox_minor.value() - 1)
        
    def increment_patch(self):
        self.spinBox_patch.setValue(self.spinBox_patch.value() + 1)
        
    def decrement_patch(self):
        if self.spinBox_patch.value() > 0:
            self.spinBox_patch.setValue(self.spinBox_patch.value() - 1)
        
    def on_major_changed(self):
        # 主版本号改变时，重置次版本号和修订号为 0
        self.spinBox_minor.setValue(0)
        self.spinBox_patch.setValue(0)
        self.update_current_version()
        
    def on_minor_changed(self):
        # 次版本号改变时，重置修订号为 0
        self.spinBox_patch.setValue(0)
        self.update_current_version()
        
    def update_current_version(self):
        major = self.spinBox_major.value()
        minor = self.spinBox_minor.value()
        patch = self.spinBox_patch.value()
        prerelease = self.comboBox_prerelease.currentText()
        prerelease_version = self.spinBox_prerelease_version.value()
        
        version = f"{major}.{minor}.{patch}"
        if prerelease != "无":
            version += f"-{prerelease}.{prerelease_version}"
        
        self.label_current_version.setText(version)
    
    def copy_version(self):
        version = self.label_current_version.text()
        QApplication.clipboard().setText(version)
        QMessageBox.information(self, "复制成功", f"版本号 {version} 已复制到剪贴板")
    
    def update_branch_name(self):
        if self.radioButton_feature.isChecked():
            branch_type = "feature"
            description = self.lineEdit_branch_description.text()
            branch_name = f"{branch_type}/{description}"
            self.lineEdit_branch_version.setVisible(False)
        elif self.radioButton_bugfix.isChecked():
            branch_type = "bugfix"
            description = self.lineEdit_branch_description.text()
            branch_name = f"{branch_type}/{description}"
            self.lineEdit_branch_version.setVisible(False)
        elif self.radioButton_hotfix.isChecked():
            branch_type = "hotfix"
            description = self.lineEdit_branch_description.text()
            branch_name = f"{branch_type}/{description}"
            self.lineEdit_branch_version.setVisible(False)
        elif self.radioButton_release.isChecked():
            branch_type = "release"
            version = self.lineEdit_branch_version.text()
            branch_name = f"{branch_type}/{version}"
            self.lineEdit_branch_version.setVisible(True)
        
        self.label_branch_name.setText(branch_name)
    
    def copy_branch(self):
        branch_name = self.label_branch_name.text()
        QApplication.clipboard().setText(branch_name)
        QMessageBox.information(self, "复制成功", f"分支名 {branch_name} 已复制到剪贴板")
    
    def update_commit_message(self):
        commit_type = self.comboBox_commit_type.currentText()
        scope = self.lineEdit_commit_scope.text()
        breaking = self.checkBox_breaking.isChecked()
        description = self.lineEdit_commit_description.text()
        body = self.textEdit_commit_body.toPlainText()
        footer = self.lineEdit_commit_footer.text()
        
        commit_message = commit_type
        if scope:
            commit_message += f"({scope})"
        if breaking:
            commit_message += "!"
        commit_message += f": {description}"
        
        if body:
            commit_message += f"\n\n{body}"
        
        if footer:
            commit_message += f"\n\n{footer}"
        
        self.textEdit_commit_message.setPlainText(commit_message)
    
    def copy_commit(self):
        commit_message = self.textEdit_commit_message.toPlainText()
        QApplication.clipboard().setText(commit_message)
        QMessageBox.information(self, "复制成功", "提交信息已复制到剪贴板")
    
    def update_changelog(self):
        version = self.lineEdit_changelog_version.text()
        date = self.dateEdit_changelog.date().toString("yyyy-MM-dd")
        added = self.textEdit_added.toPlainText().strip().split('\n')
        changed = self.textEdit_changed.toPlainText().strip().split('\n')
        fixed = self.textEdit_fixed.toPlainText().strip().split('\n')
        removed = self.textEdit_removed.toPlainText().strip().split('\n')
        
        changelog = f"# Changelog\n\n## [{version}] - {date}\n"
        
        if added and added[0]:
            changelog += "\n### Added\n"
            for item in added:
                if item.strip():
                    changelog += f"- {item.strip()}\n"
        
        if changed and changed[0]:
            changelog += "\n### Changed\n"
            for item in changed:
                if item.strip():
                    changelog += f"- {item.strip()}\n"
        
        if fixed and fixed[0]:
            changelog += "\n### Fixed\n"
            for item in fixed:
                if item.strip():
                    changelog += f"- {item.strip()}\n"
        
        if removed and removed[0]:
            changelog += "\n### Removed\n"
            for item in removed:
                if item.strip():
                    changelog += f"- {item.strip()}\n"
        
        self.textEdit_changelog.setPlainText(changelog)
    
    def use_current_version(self):
        current_version = self.label_current_version.text()
        self.lineEdit_changelog_version.setText(current_version)
        self.update_changelog()
    
    def copy_changelog(self):
        changelog = self.textEdit_changelog.toPlainText()
        QApplication.clipboard().setText(changelog)
        QMessageBox.information(self, "复制成功", "Changelog 已复制到剪贴板")
    
    def save_changelog(self):
        changelog = self.textEdit_changelog.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存 Changelog", "Changelog.md", "Markdown Files (*.md)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(changelog)
                QMessageBox.information(self, "保存成功", f"Changelog 已保存到 {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"无法保存 Changelog: {str(e)}")
    
    def save_config(self):
        # 这里可以实现保存配置的功能
        QMessageBox.information(self, "保存配置", "配置已保存")
    
    def load_config(self):
        # 这里可以实现加载配置的功能
        QMessageBox.information(self, "加载配置", "配置已加载")
    
    def show_about(self):
        QMessageBox.about(self, "关于", "版本管理工具\n基于 PySide6 开发\n用于生成版本号、分支名、提交信息和 Changelog")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VersioningUI()
    window.show()
    sys.exit(app.exec())