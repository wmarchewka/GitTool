import sys
from PySide2.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
from PySide2.QtGui import QIcon
import os

os.environ['QT_MAC_WANTS_LAYER'] = "1"


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file system view - pythonspot.com'
        self.left = 200
        self.top = 200
        self.width = 1024
        self.height = 768
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.model = QFileSystemModel()
        self.model.setRootPath('/Users/waltermarchewka/Desktop/')
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(30)
        self.tree.setSortingEnabled(False)

        self.tree.setWindowTitle("Dir View")
        self.tree.resize(1024, 768)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
