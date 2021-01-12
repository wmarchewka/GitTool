import PySide2
from PySide2 import QtGui, QtWidgets
from PySide2 import QtUiTools
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QAction, QDialog, QTableWidgetItem

import os
import signal
from logger import Logger

os.environ['QT_MAC_WANTS_LAYER'] = "1"
qtCreatorFile = 'gui/main.ui'
Ui_MainWindow, QtBaseClass = QtUiTools.loadUiType(qtCreatorFile)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.logger = Logger()
        self.log = self.logger.log
        self.log.info('{} initializing....'.format(__name__))
        self.window = None
        self.cw = None
        self.cw = self.centralWidget()
        self.startup_processes()
        self.log.info("{} init complete...".format(__name__))

    # ******************************************************************************
    def loadscreen(self):
        """loads screen from disk and shows.

        """
        try:
            self.log.info('Loading screen ' + qtCreatorFile)
            self.show()
        except FileNotFoundError:
            self.log.info("Could not find {}".format(self.guiname))

    # ******************************************************************************
    def startup_processes(self):
        self.log.info("startup processes")
        self.menu_create()
        self.loadscreen()
        self.table_setup()
        self.screen_setup()
        self.signals_and_slots()

    # ******************************************************************************
    def menu_create(self):
        """creates normal menu items for screen.

        """
        self.log.info("creating menus")
        main_menu = self.menuBar()
        main_menu.setNativeMenuBar(False)
        filemenu = main_menu.addMenu("File")
        # view_menu = main_menu.addMenu("View")
        # edit_menu = main_menu.addMenu("Edit")
        # search_menu = main_menu.addMenu("Font")
        help_menu = main_menu.addMenu("Help")

        open_action = QAction(QIcon('open.png'), "&Open", self)
        open_action.setShortcut("Ctrl+O")

        save_action = QAction(QIcon('save.png'), "&Save", self)
        save_action.setShortcut("Ctrl+S")

        exit_action = QAction(QIcon('exit.png'), "&Exit", self)
        exit_action.setShortcut("Ctrl+X")
        exit_action.triggered.connect(self.exit_app)

        help_about_action = QAction(QIcon('help.png'), "&About", self)
        help_menu.addAction(help_about_action)
        help_about_action.triggered.connect(self.help_about)

        filemenu.addAction(open_action)
        filemenu.addAction(save_action)
        filemenu.addAction(exit_action)

    # ******************************************************************************
    def signals_and_slots(self):
        """creates all signals and slots
        """
        self.log.info("signals and slots")
    # ******************************************************************************
    def help_about(self):
        help_dialog = QDialog(self)
        help_dialog.resize(300, 150)
        help_dialog.exec_()

    # ******************************************************************************
    def link_clicked(self):
        """link item was clicked. use to launch a web browser to document sheet, web page

        """
        self.log.info("Link:{}".format(self.link.text()))

    # ******************************************************************************
    def closeEvent(self, event: PySide2.QtGui.QCloseEvent) -> None:
        self.log.info("Close Event")

    # ******************************************************************************
    def screen_setup(self):
        """place any specific actions that need to be down to the  gui here
        """
        self.log.info("screen setup")
        # self.iddata.setReadOnly(True)
    # ******************************************************************************
    def table_setup(self):
        self.table_widget = self.tableWidget
        self.table_widget.setRowCount(200)
        self.table_widget.setColumnCount(7)
        self.table_widget.setItem(0, 0, QTableWidgetItem("FOLDER"))
        self.table_widget.setItem(0, 1, QTableWidgetItem("INIT"))
        self.table_widget.setItem(0, 2, QTableWidgetItem("ADD"))
        self.table_widget.setItem(0, 3, QTableWidgetItem("COMMITT"))
        self.table_widget.setItem(0, 4, QTableWidgetItem("SHOW"))
        self.table_widget.setItem(0, 5, QTableWidgetItem("PUSH"))
        self.table_widget.setItem(0, 6, QTableWidgetItem("REMOTE"))


        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

    # ******************************************************************************
    def exit_app(self):
        self.close()

    # ******************************************************************************
    def exit_signalling(self):
        """
        set up exit signalling
        :rtype: object
        """
        signal.signal(signal.SIGINT, self.exit_application)
        signal.signal(signal.SIGTERM, self.exit_application)
        self.log.debug("Setting up exit signaling...")

    # *******************************************************************************************
    def exit_application(self, signum, frame):
        """
        called when an applpication shutdown is caught
        :param signum:
        :param frame:
        """
        self.log.info("Received signal from signum: {} with frame:{}".format(signum, frame))
        self.shutdown()
