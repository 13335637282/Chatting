import os
import json
import requests
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from settings import Ui_Dialog

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # 加载配置
        self.load_settings()
        
        # 连接信号
        self.ui.select_public_key_button.clicked.connect(self.select_public_key)
        self.ui.check_server_version_button.clicked.connect(self.check_server_version)
        self.ui.check_client_version_button.clicked.connect(self.check_client_version)
        self.ui.update_client_button.clicked.connect(self.update_client)
    
    def load_settings(self):
        """加载配置文件"""
        settings_file = "settings.json"
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # 加载公钥目录
                if 'public_key_path' in settings:
                    self.ui.public_key_edit.setText(settings['public_key_path'])
                
                # 加载服务器地址
                if 'server_url' in settings:
                    self.ui.server_url_edit.setText(settings['server_url'])
                
                # 加载更新服务器地址
                if 'update_server_url' in settings:
                    self.ui.update_server_edit.setText(settings['update_server_url'])
            except (json.JSONDecodeError, IOError):
                pass
    
    def save_settings(self):
        """保存配置文件"""
        settings_file = "settings.json"
        
        settings = {
            'public_key_path': self.ui.public_key_edit.text(),
            'server_url': self.ui.server_url_edit.text(),
            'update_server_url': self.ui.update_server_edit.text()
        }
        
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def select_public_key(self):
        """选择公钥文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择公钥文件", "", "公钥文件 (*.chatting);;所有文件 (*.*)"
        )
        if file_path:
            self.ui.public_key_edit.setText(file_path)
    
    def check_server_version(self):
        """检测服务器版本"""
        server_url = self.ui.server_url_edit.text()
        if not server_url:
            QMessageBox.warning(self, "警告", "请输入服务器地址")
            return
        
        try:
            # 尝试调用服务器的版本接口
            # 假设服务器有一个 /version 接口
            url = f"{server_url}/version"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                version_data = response.json()
                server_version = version_data.get('version', '未知')
                QMessageBox.information(self, "服务器版本", f"服务器版本: {server_version}")
            else:
                QMessageBox.warning(self, "警告", f"无法获取服务器版本，状态码: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"连接服务器失败: {str(e)}")
    
    def check_client_version(self):
        """检测客户端版本"""
        # 假设客户端版本存储在某个文件中
        version_file = "version.txt"
        
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r', encoding='utf-8') as f:
                    client_version = f.read().strip()
                QMessageBox.information(self, "客户端版本", f"客户端版本: {client_version}")
            except IOError:
                QMessageBox.warning(self, "警告", "无法读取客户端版本文件")
        else:
            # 创建默认版本文件
            try:
                with open(version_file, 'w', encoding='utf-8') as f:
                    f.write("1.0.0")
                QMessageBox.information(self, "客户端版本", "客户端版本: 1.0.0 (默认版本)")
            except IOError:
                QMessageBox.warning(self, "警告", "无法创建客户端版本文件")
    
    def update_client(self):
        """更新客户端"""
        update_server = self.ui.update_server_edit.text()
        if not update_server:
            QMessageBox.warning(self, "警告", "请输入更新服务器地址")
            return
        
        try:
            # 尝试从更新服务器获取最新版本
            # 假设更新服务器有一个 /latest 接口
            url = f"{update_server}/latest"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                update_data = response.json()
                latest_version = update_data.get('version', '未知')
                download_url = update_data.get('download_url', '')
                
                if download_url:
                    reply = QMessageBox.question(
                        self, "更新客户端", 
                        f"发现新版本: {latest_version}\n是否下载更新?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    if reply == QMessageBox.Yes:
                        QMessageBox.information(self, "提示", f"正在下载更新，请稍候...\n下载地址: {download_url}")
                        # 这里可以添加下载和安装更新的逻辑
                else:
                    QMessageBox.warning(self, "警告", "未找到更新下载地址")
            else:
                QMessageBox.warning(self, "警告", f"无法获取更新信息，状态码: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"连接更新服务器失败: {str(e)}")
    
    def accept(self):
        """确认按钮点击事件"""
        if self.save_settings():
            super().accept()
        else:
            QMessageBox.critical(self, "错误", "无法保存配置文件")
