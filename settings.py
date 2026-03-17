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
    QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 512, 295))
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
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_2 = QScrollArea(self.tab_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 512, 295))
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
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 512, 295))
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

        self.tabWidget.setCurrentIndex(0)


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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"\u542f\u52a8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"\u5176\u4ed6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Dialog", u"\u5173\u4e8e", None))
    # retranslateUi

