# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_users.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, Qt,
                            QTime, QUrl)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog,
                               QFrame, QHBoxLayout, QLineEdit, QListView,
                               QSizePolicy, QToolButton, QVBoxLayout, QWidget)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(508, 696)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.toolButton = QToolButton(self.frame_2)
        self.toolButton.setObjectName("toolButton")

        self.horizontalLayout.addWidget(self.toolButton)

        self.toolButton_2 = QToolButton(self.frame_2)
        self.toolButton_2.setObjectName("toolButton_2")

        self.horizontalLayout.addWidget(self.toolButton_2)

        self.verticalLayout_2.addWidget(self.frame_2)

        self.listView = QListView(Dialog)
        self.listView.setObjectName("listView")
        self.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_2.addWidget(self.listView)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "\u641c\u7d22\u7528\u6237", None)
        )
        self.toolButton.setText(
            QCoreApplication.translate("Dialog", "\u641c\u7d22", None)
        )
        self.toolButton_2.setText(
            QCoreApplication.translate(
                "Dialog", "\u597d\u53cb\u8bf7\u6c42\u5217\u8868", None
            )
        )

    # retranslateUi
