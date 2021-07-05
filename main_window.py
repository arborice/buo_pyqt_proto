from typing import List
from bindings import parseBuoOutput
from buo_py_bindings import get_buo_output
from focused_cache_widget import TopCachedWidget
from PyQt5.QtCore import Qt, QSize, QStringListModel, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QVBoxLayout, QSizePolicy, QListView

DEBOUNCE_INTERVAL = 600


class BuoPrototype(QMainWindow):
    debouncer: QTimer

    def __init__(self):
        super().__init__()
        self.debouncer = QTimer(self)
        self.debouncer.setSingleShot(True)

        self.setupUiElems()
        self.setupUiLayout()

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

    def setupUiElems(self):
        self.setWindowTitle('Buo Prototype')
        self.setObjectName('Buo Main Window')

        central_widget = QWidget()
        central_widget.setObjectName('Central Widget')
        self.setCentralWidget(central_widget)

        self.cache_query = QLineEdit(self)
        self.cache_query.setPlaceholderText('search!')
        self.cache_query.textEdited.connect(self.updateTopWidget)

        self.top_cached_widget = TopCachedWidget(self)

        self.cache_hit_list = QListView(self)
        self.cache_hit_list.setBatchSize(50)
        self.cache_hit_list.setUniformItemSizes(True)
        self.cache_hit_list.setViewMode(QListView.ListMode)
        self.cache_hit_list.setResizeMode(QListView.Fixed)
        self.cache_hit_list.setItemAlignment(Qt.AlignHCenter)

        self.cache_hit_model = QStringListModel(self.cache_hit_list)

        #  self.toggle_cached_only = QCheckBox('List cached items only?')

    def setupUiLayout(self):
        self.setMinimumSize(QSize(560, 320))

        central_layout = QVBoxLayout()
        main_layout = QVBoxLayout()

        line_input_size_policy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        line_input_size_policy.setVerticalStretch(1)
        self.cache_query.setSizePolicy(line_input_size_policy)

        main_layout.addWidget(self.cache_query)
        main_layout.insertSpacing(0, 10)

        top_widget_size_policy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        top_widget_size_policy.setVerticalStretch(9)
        self.top_cached_widget.setSizePolicy(top_widget_size_policy)

        main_layout.addWidget(self.top_cached_widget)
        main_layout.addWidget(self.cache_hit_list)

        central_layout.addChildLayout(main_layout)
        self.centralWidget().setLayout(central_layout)
