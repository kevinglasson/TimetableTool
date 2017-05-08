# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\login_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    # QT designer generated stuff
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(430, 323)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.title = QtGui.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(100, 50, 221, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.title.setFont(font)
        self.title.setObjectName(_fromUtf8("title"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(80, 150, 261, 104))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        # Relevant stuff!

        # Username label
        self.user_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.user_lbl.setFont(font)
        self.user_lbl.setObjectName(_fromUtf8("user_lbl"))
        self.verticalLayout.addWidget(self.user_lbl)

        # Password label
        self.pass_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pass_lbl.setFont(font)
        self.pass_lbl.setObjectName(_fromUtf8("pass_lbl"))
        self.verticalLayout.addWidget(self.pass_lbl)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        # Username field
        self.user_field = QtGui.QLineEdit(self.layoutWidget)
        self.user_field.setObjectName(_fromUtf8("user_field"))
        self.verticalLayout_2.addWidget(self.user_field)

        # Password field
        self.pass_field = QtGui.QLineEdit(self.layoutWidget)
        self.pass_field.setEchoMode(QtGui.QLineEdit.Password)
        self.pass_field.setObjectName(_fromUtf8("pass_field"))
        self.verticalLayout_2.addWidget(self.pass_field)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        # Login button
        self.login_btn = QtGui.QPushButton(self.layoutWidget)
        self.login_btn.setObjectName(_fromUtf8("login_btn"))
        self.verticalLayout_3.addWidget(self.login_btn)
        MainWindow.setCentralWidget(self.centralwidget)

        # This method sets all the text / connections etc that were made in the
        # GUI designer
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Timetable Tool", None))
        self.title.setText(_translate("MainWindow", "OASIS Login", None))
        self.user_lbl.setText(_translate("MainWindow", "USERNAME", None))
        self.pass_lbl.setText(_translate("MainWindow", "PASSWORD", None))
        self.login_btn.setText(_translate("MainWindow", "Login", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
