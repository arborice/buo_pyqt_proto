# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from typing import List
from bindings import parseBuoOutput
from buo_py_bindings import get_buo_output
from focused_cache_widget import TopCachedWidget
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QStringListModel, QTimer, QMetaObject, QCoreApplication, QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QSizePolicy, QListView, QLabel, QScrollArea, QFrame, QGridLayout

DEBOUNCE_INTERVAL = 600


class BuoPrototype(QMainWindow):
    debouncer: QTimer

    def __init__(self):
        super().__init__()
        self.debouncer = QTimer(self)
        self.debouncer.setSingleShot(True)

        self.setupUi()
        self.cache_hit_model = QStringListModel(self.cache_hit_list)
        self.scrollArea.setHidden(True)

    def debounceEvent(self, callback):
        self.debouncer.timeout.connect(callback)
        self.debouncer.start(DEBOUNCE_INTERVAL)

    def updateTopWidget(self, query: str):
        def debouncedUpdate():
            try:
                buo_response = get_buo_output(query)
                parsed_response = parseBuoOutput(buo_response)
                self.top_cached_widget.update(parsed_response)
            except Exception as E:
                print(E)

        self.debounceEvent(debouncedUpdate)

    def refreshCacheHitList(self, items: List[str]):
        self.cache_hit_model.setStringList(items)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(560, 600)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(560, 320))
        self.setMaximumSize(QSize(560, 600))
        font = QFont()
        font.setFamily("Inter Light")
        font.setPointSize(10)
        self.setFont(font)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        icon = QIcon()
        icon.addPixmap(QPixmap(
            "../../../../Pictures/Link to Pictures/155410143_3717931704964661_1567340756741086546_n.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cache_query = QLineEdit(self.centralwidget)
        self.cache_query.setContextMenuPolicy(Qt.NoContextMenu)
        self.cache_query.setObjectName("cache_query")
        self.horizontalLayout.addWidget(self.cache_query)
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.top_cached_widget = TopCachedWidget(self)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(
            self.top_cached_widget.sizePolicy().hasHeightForWidth())
        self.top_cached_widget.setSizePolicy(sizePolicy)
        self.top_cached_widget.setObjectName("top_cached_widget")
        self.verticalLayout.addWidget(self.top_cached_widget)

        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.scrollArea = QScrollArea(self.centralwidget)
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(9)
        sizePolicy.setHeightForWidth(
            self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 544, 429))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.cache_hit_list = QListView(
            self.scrollAreaWidgetContents)
        self.cache_hit_list.setContextMenuPolicy(Qt.NoContextMenu)
        self.cache_hit_list.setObjectName("cache_hit_list")
        self.gridLayout.addWidget(self.cache_hit_list, 1, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _t = QCoreApplication.translate
        self.setWindowTitle(_t("MainWindow", "Buo Prototype"))
        self.checkBox.setText("")
