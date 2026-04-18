# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(584, 376)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabBarAutoHide(True)
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.verticalLayout_2 = QVBoxLayout(self.tab_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.tab_1)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 540, 310))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.theme_frame = QFrame(self.scrollAreaWidgetContents)
        self.theme_frame.setObjectName(u"theme_frame")
        self.theme_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.theme_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.theme_frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.theme_label = QLabel(self.theme_frame)
        self.theme_label.setObjectName(u"theme_label")

        self.verticalLayout_7.addWidget(self.theme_label)

        self.light_theme_radio = QRadioButton(self.theme_frame)
        self.light_theme_radio.setObjectName(u"light_theme_radio")

        self.verticalLayout_7.addWidget(self.light_theme_radio)

        self.dark_theme_radio = QRadioButton(self.theme_frame)
        self.dark_theme_radio.setObjectName(u"dark_theme_radio")

        self.verticalLayout_7.addWidget(self.dark_theme_radio)


        self.verticalLayout_6.addWidget(self.theme_frame)

        self.font_frame = QFrame(self.scrollAreaWidgetContents)
        self.font_frame.setObjectName(u"font_frame")
        self.font_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.font_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.font_frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.font_label = QLabel(self.font_frame)
        self.font_label.setObjectName(u"font_label")

        self.verticalLayout_8.addWidget(self.font_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.font_family_label = QLabel(self.font_frame)
        self.font_family_label.setObjectName(u"font_family_label")

        self.horizontalLayout.addWidget(self.font_family_label)

        self.font_family_combo = QComboBox(self.font_frame)
        self.font_family_combo.setObjectName(u"font_family_combo")

        self.horizontalLayout.addWidget(self.font_family_combo)

        self.select_font_file_button = QPushButton(self.font_frame)
        self.select_font_file_button.setObjectName(u"select_font_file_button")

        self.horizontalLayout.addWidget(self.select_font_file_button)


        self.verticalLayout_8.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.font_size_label = QLabel(self.font_frame)
        self.font_size_label.setObjectName(u"font_size_label")

        self.horizontalLayout_2.addWidget(self.font_size_label)

        self.font_size_spin = QSpinBox(self.font_frame)
        self.font_size_spin.setObjectName(u"font_size_spin")
        self.font_size_spin.setMinimum(8)
        self.font_size_spin.setMaximum(72)
        self.font_size_spin.setValue(12)

        self.horizontalLayout_2.addWidget(self.font_size_spin)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.apply_font_button = QPushButton(self.font_frame)
        self.apply_font_button.setObjectName(u"apply_font_button")

        self.verticalLayout_8.addWidget(self.apply_font_button)


        self.verticalLayout_6.addWidget(self.font_frame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_1, "")
        self.tab_network = QWidget()
        self.tab_network.setObjectName(u"tab_network")
        self.verticalLayout_network = QVBoxLayout(self.tab_network)
        self.verticalLayout_network.setObjectName(u"verticalLayout_network")
        self.scrollArea_network = QScrollArea(self.tab_network)
        self.scrollArea_network.setObjectName(u"scrollArea_network")
        self.scrollArea_network.setWidgetResizable(True)
        self.scrollAreaWidgetContents_network = QWidget()
        self.scrollAreaWidgetContents_network.setObjectName(u"scrollAreaWidgetContents_network")
        self.scrollAreaWidgetContents_network.setGeometry(QRect(0, 0, 540, 310))
        self.verticalLayout_network_content = QVBoxLayout(self.scrollAreaWidgetContents_network)
        self.verticalLayout_network_content.setObjectName(u"verticalLayout_network_content")
        self.network_frame = QFrame(self.scrollAreaWidgetContents_network)
        self.network_frame.setObjectName(u"network_frame")
        self.network_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.network_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_network_settings = QVBoxLayout(self.network_frame)
        self.verticalLayout_network_settings.setObjectName(u"verticalLayout_network_settings")
        self.network_label = QLabel(self.network_frame)
        self.network_label.setObjectName(u"network_label")

        self.verticalLayout_network_settings.addWidget(self.network_label)

        self.horizontalLayout_public_key = QHBoxLayout()
        self.horizontalLayout_public_key.setObjectName(u"horizontalLayout_public_key")
        self.public_key_label = QLabel(self.network_frame)
        self.public_key_label.setObjectName(u"public_key_label")

        self.horizontalLayout_public_key.addWidget(self.public_key_label)

        self.public_key_edit = QLineEdit(self.network_frame)
        self.public_key_edit.setObjectName(u"public_key_edit")

        self.horizontalLayout_public_key.addWidget(self.public_key_edit)

        self.select_public_key_button = QPushButton(self.network_frame)
        self.select_public_key_button.setObjectName(u"select_public_key_button")

        self.horizontalLayout_public_key.addWidget(self.select_public_key_button)


        self.verticalLayout_network_settings.addLayout(self.horizontalLayout_public_key)

        self.horizontalLayout_server_url = QHBoxLayout()
        self.horizontalLayout_server_url.setObjectName(u"horizontalLayout_server_url")
        self.server_url_label = QLabel(self.network_frame)
        self.server_url_label.setObjectName(u"server_url_label")

        self.horizontalLayout_server_url.addWidget(self.server_url_label)

        self.server_url_edit = QLineEdit(self.network_frame)
        self.server_url_edit.setObjectName(u"server_url_edit")

        self.horizontalLayout_server_url.addWidget(self.server_url_edit)


        self.verticalLayout_network_settings.addLayout(self.horizontalLayout_server_url)

        self.horizontalLayout_update_server = QHBoxLayout()
        self.horizontalLayout_update_server.setObjectName(u"horizontalLayout_update_server")
        self.update_server_label = QLabel(self.network_frame)
        self.update_server_label.setObjectName(u"update_server_label")

        self.horizontalLayout_update_server.addWidget(self.update_server_label)

        self.update_server_edit = QLineEdit(self.network_frame)
        self.update_server_edit.setObjectName(u"update_server_edit")

        self.horizontalLayout_update_server.addWidget(self.update_server_edit)


        self.verticalLayout_network_settings.addLayout(self.horizontalLayout_update_server)

        self.check_server_version_button = QPushButton(self.network_frame)
        self.check_server_version_button.setObjectName(u"check_server_version_button")

        self.verticalLayout_network_settings.addWidget(self.check_server_version_button)

        self.check_client_version_button = QPushButton(self.network_frame)
        self.check_client_version_button.setObjectName(u"check_client_version_button")

        self.verticalLayout_network_settings.addWidget(self.check_client_version_button)

        self.update_client_button = QPushButton(self.network_frame)
        self.update_client_button.setObjectName(u"update_client_button")

        self.verticalLayout_network_settings.addWidget(self.update_client_button)

        self.buttons = QFrame(self.network_frame)
        self.buttons.setObjectName(u"buttons")
        self.buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.buttons)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ok_button = QPushButton(self.buttons)
        self.ok_button.setObjectName(u"ok_button")

        self.horizontalLayout_3.addWidget(self.ok_button)

        self.cancel_button = QPushButton(self.buttons)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontalLayout_3.addWidget(self.cancel_button)


        self.verticalLayout_network_settings.addWidget(self.buttons)


        self.verticalLayout_network_content.addWidget(self.network_frame)

        self.verticalSpacer_network = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_network_content.addItem(self.verticalSpacer_network)

        self.scrollArea_network.setWidget(self.scrollAreaWidgetContents_network)

        self.verticalLayout_network.addWidget(self.scrollArea_network)

        self.tabWidget.addTab(self.tab_network, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_2 = QScrollArea(self.tab_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 540, 310))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea_3 = QScrollArea(self.tab_3)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 540, 310))
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_4.addWidget(self.scrollArea_3)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_5 = QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.credits_text_browser = QTextBrowser(self.tab_4)
        self.credits_text_browser.setObjectName(u"credits_text_browser")
        self.credits_text_browser.setOpenExternalLinks(True)

        self.verticalLayout_5.addWidget(self.credits_text_browser)

        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u8bbe\u7f6e", None))
        self.theme_label.setText(QCoreApplication.translate("Dialog", u"\u4e3b\u9898", None))
        self.light_theme_radio.setText(QCoreApplication.translate("Dialog", u"\u6d45\u8272", None))
        self.dark_theme_radio.setText(QCoreApplication.translate("Dialog", u"\u6df1\u8272", None))
        self.font_label.setText(QCoreApplication.translate("Dialog", u"\u5b57\u4f53", None))
        self.font_family_label.setText(QCoreApplication.translate("Dialog", u"\u5b57\u4f53\uff1a", None))
        self.select_font_file_button.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9\u5b57\u4f53\u6587\u4ef6", None))
        self.font_size_label.setText(QCoreApplication.translate("Dialog", u"\u5927\u5c0f\uff1a", None))
        self.apply_font_button.setText(QCoreApplication.translate("Dialog", u"\u5e94\u7528\u5b57\u4f53", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("Dialog", u"\u754c\u9762", None))
        self.network_label.setText(QCoreApplication.translate("Dialog", u"\u7f51\u7edc\u8bbe\u7f6e", None))
        self.public_key_label.setText(QCoreApplication.translate("Dialog", u"\u516c\u94a5\u76ee\u5f55\uff1a", None))
        self.public_key_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8f93\u5165\u516c\u94a5\u6587\u4ef6\u8def\u5f84", None))
        self.select_public_key_button.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8", None))
        self.server_url_label.setText(QCoreApplication.translate("Dialog", u"\u670d\u52a1\u5668\u5730\u5740\uff1a", None))
        self.server_url_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"http://127.0.0.1:5000/api/v1", None))
        self.update_server_label.setText(QCoreApplication.translate("Dialog", u"\u66f4\u65b0\u670d\u52a1\u5668\uff1a", None))
        self.update_server_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"http://127.0.0.1:5000/update", None))
        self.check_server_version_button.setText(QCoreApplication.translate("Dialog", u"\u68c0\u6d4b\u670d\u52a1\u5668\u7248\u672c", None))
        self.check_client_version_button.setText(QCoreApplication.translate("Dialog", u"\u68c0\u6d4b\u5ba2\u6237\u7aef\u7248\u672c", None))
        self.update_client_button.setText(QCoreApplication.translate("Dialog", u"\u66f4\u65b0\u5ba2\u6237\u7aef", None))
        self.ok_button.setText(QCoreApplication.translate("Dialog", u"\u5e94\u7528", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_network), QCoreApplication.translate("Dialog", u"\u7f51\u7edc", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"\u542f\u52a8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"\u5176\u4ed6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Dialog", u"\u5173\u4e8e", None))
    # retranslateUi

