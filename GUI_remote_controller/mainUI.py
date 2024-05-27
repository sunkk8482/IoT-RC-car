# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1039, 730)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.leftButton = QPushButton(self.centralwidget)
        self.leftButton.setObjectName(u"leftButton")
        self.leftButton.setGeometry(QRect(50, 400, 75, 51))
        self.logText = QPlainTextEdit(self.centralwidget)
        self.logText.setObjectName(u"logText")
        self.logText.setGeometry(QRect(70, 40, 441, 261))
        font = QFont()
        font.setFamilies([u"Consolas"])
        self.logText.setFont(font)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 20, 121, 16))
        self.midButton = QPushButton(self.centralwidget)
        self.midButton.setObjectName(u"midButton")
        self.midButton.setGeometry(QRect(140, 400, 75, 51))
        self.rightButton = QPushButton(self.centralwidget)
        self.rightButton.setObjectName(u"rightButton")
        self.rightButton.setGeometry(QRect(230, 400, 75, 51))
        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName(u"backButton")
        self.backButton.setGeometry(QRect(140, 460, 75, 51))
        self.goButton = QPushButton(self.centralwidget)
        self.goButton.setObjectName(u"goButton")
        self.goButton.setGeometry(QRect(140, 340, 75, 51))
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(370, 440, 111, 71))
        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(370, 340, 111, 71))
        self.stopButton.setCursor(QCursor(Qt.ArrowCursor))
        self.textinput = QTextEdit(self.centralwidget)
        self.textinput.setObjectName(u"textinput")
        self.textinput.setGeometry(QRect(530, 40, 441, 261))
        self.enterButton = QPushButton(self.centralwidget)
        self.enterButton.setObjectName(u"enterButton")
        self.enterButton.setGeometry(QRect(900, 310, 75, 41))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(530, 20, 121, 16))
        self.nowcmd = QLabel(self.centralwidget)
        self.nowcmd.setObjectName(u"nowcmd")
        self.nowcmd.setGeometry(QRect(100, 560, 341, 91))
        font1 = QFont()
        font1.setPointSize(24)
        self.nowcmd.setFont(font1)
        self.nowcmd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(530, 370, 50, 16))
        self.ansText = QPlainTextEdit(self.centralwidget)
        self.ansText.setObjectName(u"ansText")
        self.ansText.setGeometry(QRect(530, 390, 441, 261))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1039, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.startButton.clicked.connect(MainWindow.start)
        self.stopButton.clicked.connect(MainWindow.stop)
        self.rightButton.clicked.connect(MainWindow.right)
        self.goButton.clicked.connect(MainWindow.go)
        self.midButton.clicked.connect(MainWindow.mid)
        self.backButton.clicked.connect(MainWindow.back)
        self.leftButton.clicked.connect(MainWindow.left)
        self.enterButton.clicked.connect(MainWindow.enter)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.leftButton.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"command Table", None))
        self.midButton.setText(QCoreApplication.translate("MainWindow", u"Mid", None))
        self.rightButton.setText(QCoreApplication.translate("MainWindow", u"Right", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.goButton.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.enterButton.setText(QCoreApplication.translate("MainWindow", u"\uc9c8\ubb38\ud558\uae30", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"AI\uc5d0\uac8c \ubb3c\uc5b4\ubcf4\uc138\uc694!", None))
        self.nowcmd.setText(QCoreApplication.translate("MainWindow", u"Now Command", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\ub2f5\ubcc0", None))
    # retranslateUi

