# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_friends.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QHBoxLayout, QLineEdit, QListView, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(546, 697)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.toolButton = QToolButton(self.frame_2)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.listView = QListView(Dialog)
        self.listView.setObjectName(u"listView")
        self.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_2.addWidget(self.listView)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u641c\u7d22\u7528\u6237", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"\u641c\u7d22", None))
    # retranslateUi

