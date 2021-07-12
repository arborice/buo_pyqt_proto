from typing import Union
from bindings import DirMeta, MediaMeta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel


class TopCachedWidget(QLabel):
    data: Union[DirMeta, MediaMeta, None]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.setupUiFlags()

    def hydrateLabels(self):
        if isinstance(self.data, MediaMeta):
            rich_txt = self.data.file_name
            if self.data.title is not None:
                rich_txt += f"\ntitle: {self.title}"
            if self.data.author is not None:
                rich_txt += f"\nauthor: {self.author}"
            if self.data.date is not None:
                rich_txt += f"\ndate: {self.date}"
            if self.data.duration is not None:
                rich_txt += f"\nduration: {self.duration}"

            if self.data.stats is not None:
                rich_txt = f"\ncode breakdown:\n"
                rich_txt += "\n".join([str(stat)
                                       for stat in self.data.stats])

            if self.data.display_extra and self.data.extra is not None:
                rich_txt += f"\n{self.data.extra}"

            self.setText(rich_txt)

        elif isinstance(self.data, DirMeta):
            self.main_label.setText(str(self.data))

    def update(self, data: Union[DirMeta, MediaMeta, None]):
        self.data = data
        self.hydrateLabels()

    def hide(self):
        self.setHidden(True)

    def clear(self):
        """use this method instead of setting data to None"""
        self.update(None)

    def setupUiFlags(self):
        self.setCursor(
            QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.WheelFocus)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setAutoFillBackground(True)
        self.setTextFormat(Qt.MarkdownText)
        self.setOpenExternalLinks(True)
        self.setTextInteractionFlags(
            Qt.LinksAccessibleByKeyboard | Qt.LinksAccessibleByMouse)
