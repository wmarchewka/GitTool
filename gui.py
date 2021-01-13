import PySide2
from PySide2 import QtGui, QtWidgets
from PySide2 import QtUiTools
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QAction, QDialog, QTableWidgetItem, QFileDialog

import os
import signal
from logger import Logger

os.environ['QT_MAC_WANTS_LAYER'] = "1"
qtCreatorFile = 'gui/main.ui'
Ui_MainWindow, QtBaseClass = QtUiTools.loadUiType(qtCreatorFile)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, main, data):
        super(MainWindow, self).__init__()
        self.selected_item = None
        self.setupUi(self)
        self.logger = Logger()
        self.main = main
        self.data = data
        self.log = self.logger.log
        self.log.info('{} initializing....'.format(__name__))
        self.startup_processes()
        self.log.info("{} init complete...".format(__name__))

    def load_screen(self):
        """loads screen from disk and shows.
        """
        try:
            self.log.info('Loading screen ' + qtCreatorFile)
            self.show()
        except FileNotFoundError:
            self.log.info("Could not find {}".format(self.guiname))

    def startup_processes(self):
        self.log.info("startup processes")
        self.menu_create()
        self.load_screen()
        self.table_setup()
        self.screen_setup()
        self.signals_and_slots()

    def signals_and_slots(self):
        """creates all signals and slots
        tb=table, pb=pushbutton, te=textedit, rb=radiobutton
        """
        self.log.info("signals and slots")
        self.tb_Repos.cellClicked.connect(self.table_clicked)
        self.tb_Repos.horizontalHeader().sectionClicked.connect(self.horizontal_header_clicked)
        self.tb_Repos.verticalHeader().sectionClicked.connect(self.vertical_header_clicked)
        self.te_token.textChanged.connect(self.te_token_text_changed)
        self.pb_delete_all_git_local.clicked.connect(self.pb_delete_all_git_local_clicked)
        self.pb_delete_selected_local_git.clicked.connect(self.pb_delete_selected_local_git_clicked)
        self.pb_set_local_path.clicked.connect(self.set_local_path_clicked)
        self.pb_create_connection.clicked.connect(self.pb_create_connection_clicked)
        self.pb_get_local_folders.clicked.connect(self.pb_get_local_folders_clicked)
        self.pb_add_all_to_remote.clicked.connect(self.pb_add_all_to_remote_clicked)
        self.rb_siemens_url.clicked.connect(self.radio_button_pushed)
        self.rb_gitlab_url.clicked.connect(self.radio_button_pushed)

    def pb_create_connection_clicked(self):
        pass

    def set_local_path_clicked(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        self.data.top_level_path = QFileDialog.getExistingDirectory(None, 'Set Directory', )
        self.te_local_path.setText(str(self.data.top_level_path))

    def table_clicked(self, row, column):
        # FOLDER, INIT, ADD, COMMIT, SHOW, PUSH, REMOTE
        self.log.info("TABLE CLICKED:  ROW: {}  COL: {}".format(row, column))
        self.selected_item = row, column
        self.tb_Repos.clearSelection()
        if column == 1:  # init
            self.main.gitCommands.init(path=self.data.top_level_folders[row - 1], row=row - 1)
            self.main.gitCommands.init_check(path=self.data.top_level_folders[row - 1])
        if column == 2:  # add
            self.main.gitCommands.add(path=self.data.top_level_folders[row - 1], row=row - 1)
            self.main.folderCommands.add_check(row)
        if column == 3:  # commit
            self.main.gitCommands.commit(path=self.data.top_level_folders[row - 1], row=row - 1)
            self.main.folderCommands.commit_check(row)

    def horizontal_header_clicked(self, index):
        self.log.info("Horizontal index:{}".format(index))
        self.horizontal_column_selected = index

    def vertical_header_clicked(self, index):
        self.log.info("Vertical index:{}".format(index))
        self.vertical_row_selected = index

    def te_token_text_changed(self):
        self.token = self.te_token.toPlainText()

    def pb_delete_all_git_local_clicked(self):
        self.main.delete_all_git_local()

    def radio_button_pushed(self):
        if self.rb_siemens_url.isChecked():
            self.url = self.siemens_txt_url
        elif self.rb_gitlab_url.isChecked():
            self.url = self.gitlab_txt_url

    def pb_delete_selected_local_git_clicked(self):
        pass

    def pb_get_local_folders_clicked(self):
        self.main.folderCommands.get_folder_list()
        self.main.folderCommands.startup_check()

    def pb_add_all_to_remote_clicked(self):
        pass

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

    def help_about(self):
        help_dialog = QDialog(self)
        help_dialog.resize(300, 150)
        help_dialog.exec_()

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent) -> None:
        self.log.info("Close Event")

    def screen_setup(self):
        """place any specific actions that need to be down to the  gui here
        """
        self.log.info("screen setup")
        # self.iddata.setReadOnly(True)

    def table_setup(self):
        self.tb_Repos = self.tb_Repos
        self.tb_Repos.setRowCount(200)
        self.tb_Repos.setColumnCount(7)
        self.tb_Repos.setItem(0, 0, QTableWidgetItem("FOLDER"))
        self.tb_Repos.setItem(0, 1, QTableWidgetItem("INIT"))
        self.tb_Repos.setItem(0, 2, QTableWidgetItem("ADD"))
        self.tb_Repos.setItem(0, 3, QTableWidgetItem("COMMITT"))
        self.tb_Repos.setItem(0, 4, QTableWidgetItem("SHOW"))
        self.tb_Repos.setItem(0, 5, QTableWidgetItem("PUSH"))
        self.tb_Repos.setItem(0, 6, QTableWidgetItem("REMOTE"))
        header = self.tb_Repos.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

    def exit_app(self):
        self.close()

    def exit_signalling(self):
        """
        set up exit signalling
        :rtype: object
        """
        signal.signal(signal.SIGINT, self.exit_application)
        signal.signal(signal.SIGTERM, self.exit_application)
        self.log.debug("Setting up exit signaling...")

    def exit_application(self, signum, frame):
        """
        called when an application shutdown is caught
        :param signum:
        :param frame:
        """
        self.log.info("Received signal from signum: {} with frame:{}".format(signum, frame))
        self.shutdown()

    def table_set_item_text(self, row, column, text):
        self.tb_Repos.setItem(row, column, QTableWidgetItem(text))

    def table_set_item_background(self, row, column, color):
        background_color = None
        if color == 'green':
            background_color = self.data.color_green
        if color == 'red':
            background_color = self.data.color_red
        # self.tb_Repos.item(row, column).setBackground(background_color)
        self.tb_Repos.item(row, column).setBackground(background_color)
