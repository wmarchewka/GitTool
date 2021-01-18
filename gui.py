import PySide2
from PySide2 import QtGui, QtWidgets
from PySide2 import QtUiTools
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QAction, QDialog, QTableWidgetItem, QFileDialog, QDesktopWidget, QWidget
from PySide2 import QtCore
import threading
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
        self.log.debug('{} initializing....'.format(__name__))
        self.startup_processes()
        self.log.debug("{} init complete...".format(__name__))

    def load_screen(self):
        """loads screen from disk and shows.
        """
        try:
            self.log.debug('Loading screen ' + qtCreatorFile)
            self.show()
            self.monitor_set(1, self)
        except FileNotFoundError:
            self.log.debug("Could not find {}".format(self.guiname))

    def startup_processes(self):
        self.log.debug("startup processes")
        self.signals_and_slots()
        self.menu_create()
        self.load_screen()
        self.table_setup()
        self.screen_setup()

    def signals_and_slots(self):
        """creates all signals and slots
        tb=table, pb=pushbutton, te=textedit, rb=radiobutton
        """
        self.log.debug("GUI create signals and slots")
        self.tb_Repos.cellClicked.connect(self.table_clicked)
        self.tb_Repos.horizontalHeader().sectionClicked.connect(self.horizontal_header_clicked)
        self.tb_Repos.verticalHeader().sectionClicked.connect(self.vertical_header_clicked)
        self.te_token.textChanged.connect(self.te_token_text_changed)
        self.pb_delete_selected_local_git.clicked.connect(self.pb_delete_selected_local_git_clicked)
        self.pb_delete_selected_remote_git.clicked.connect(self.pb_delete_selected_remote_git_clicked)
        self.pb_set_local_path.clicked.connect(self.set_local_path_clicked)
        self.pb_get_local_folders.clicked.connect(self.pb_get_local_folders_clicked)
        self.pb_create_and_push.clicked.connect(self.create_and_push)
        self.rb_siemens_url.toggled.connect(self.radio_button_pushed)
        self.rb_gitlab_url.toggled.connect(self.radio_button_pushed)
        # self.pb_delete_all_git_local.clicked.connect(self.pb_delete_all_git_local_clicked)
        # self.pb_create_connection.clicked.connect(self.pb_create_connection_clicked)
        # self.pb_add_all_to_remote.clicked.connect(self.pb_add_all_to_remote_clicked)

    def create_and_push(self):
        self.log.debug('Create and push')
        rows = self.vertical_selection
        create_and_push_thread = threading.Thread(target=self.main.folderCommands.add_folder_to_remote, args=(rows,))
        create_and_push_thread.start()
        # self.main.folderCommands.add_folder_to_remote(rows=rows)
        self.tb_Repos.clearSelection()

    def set_local_path_clicked(self):
        self.log.debug("Local PATH clicked")
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        self.data.top_level_path = QFileDialog.getExistingDirectory(None, 'Set Directory', )
        self.te_local_path.setText(str(self.data.top_level_path))

    def table_clicked(self, row, column):
        # FOLDER, INIT, ADD, COMMIT, SHOW, PUSH, REMOTE
        self.log.debug("TABLE CLICKED:  ROW: {}  COL: {}".format(row, column))
        self.selected_item = row, column
        self.tb_Repos.clearSelection()
        self.log.debug("********************************************************************************************")
        if self.check_data_exists(row):
            if column == 1:  # init
                self.main.gitCommands.init(path=self.data.top_level_folders[row - 1], row=row - 1)
                self.main.folderCommands.init_check(row)
            if column == 2:  # add
                self.main.gitCommands.add(path=self.data.top_level_folders[row - 1], row=row - 1)
                self.main.folderCommands.add_check(row)
            if column == 3:  # commit
                self.main.gitCommands.commit(path=self.data.top_level_folders[row - 1], row=row - 1)
                self.main.folderCommands.commit_check(row)
            if column == 4:  # remote
                self.main.gitCommands.remote(path=self.data.top_level_folders[row - 1], row=row - 1)
                self.main.folderCommands.remote_check(row)
            if column == 5:  # push
                self.main.gitCommands.push(path=self.data.top_level_folders[row - 1], row=row - 1)
                self.main.folderCommands.push_check(row)
            if column == 6:  # commit
                self.main.gitCommands.repo_check(path=self.data.top_level_folders[row - 1], row=row - 1)
                self.main.folderCommands.repo_check(row)
        self.tb_Repos.clearSelection()

    def horizontal_header_clicked(self, index):
        self.log.debug("Horizontal header clicked  Index:{}".format(index))
        self.horizontal_column_selected = index

    def vertical_header_clicked(self, index):
        self.log.debug("Vertical header clicked   Index:{}".format(index))
        if self.check_data_exists(index):
            self.vertical_row_selected = index
            self.vertical_selection = []
            indexes = self.tb_Repos.selectionModel().selectedRows()
            for index in sorted(indexes):
                self.log.debug('Row %d is selected' % index.row())
                self.vertical_selection.append(index.row())
            self.log.debug("Vertical selection:{}".format(self.vertical_selection))

    def te_token_text_changed(self):
        self.data.token = self.te_token.toPlainText()

    def pb_delete_all_git_local_clicked(self):
        self.main.delete_all_git_local()

    def radio_button_pushed(self):
        self.log.debug("Radio Button pushed")
        if self.rb_siemens_url.isChecked():
            self.data.url = self.data.siemens_txt_url
            self.gui.te_token.setText(self.data.siemens_private_token)
            self.log.debug("Siemens URL selected")
        elif self.rb_gitlab_url.isChecked():
            self.data.url = self.data.gitlab_txt_url
            self.te_token.setText(self.data.gitlab_private_token)
            self.log.debug("GITLAB URL selected")

    def pb_delete_selected_remote_git_clicked(self):
        rows = self.vertical_selection
        self.main.folderCommands.delete_selected_remote_git(rows)
        self.tb_Repos.clearSelection()

    def pb_delete_selected_local_git_clicked(self):
        rows = self.vertical_selection
        self.main.folderCommands.delete_selected_local_git(rows)
        self.tb_Repos.clearSelection()

    def pb_get_local_folders_clicked(self):
        self.log.debug("GIT Local Folders clicked")
        get_folders_thread = threading.Thread(target=self.get_all_folders_thread)
        get_folders_thread.start()
        self.tb_Repos.clearSelection()

    def get_all_folders_thread(self):
        self.main.folderCommands.get_folder_list()
        self.main.folderCommands.check_all_folders()

    def check_data_exists(self, row):
        self.log.debug("check if data exists")
        try:
            if self.data.top_level_folders[row - 1]:
                result = True
            else:
                result = False
        except IndexError as error:
            self.log.debug("check data exists ERROR:{}".format(error))
            result = False
        else:
            result = True
        return result

    def pb_add_all_to_remote_clicked(self):
        pass

    def menu_create(self):
        """creates normal menu items for screen.

        """
        self.log.debug("creating menus")
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
        self.log.debug("Close Event")

    def screen_setup(self):
        """place any specific actions that need to be down to the  gui here
        """
        self.log.debug("screen setup")
        self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, 'files'))
        self.rb_gitlab_url.setChecked(True)

    def table_setup(self):
        self.log.debug("Table Names Setup")
        self.tb_Repos = self.tb_Repos
        self.tb_Repos.setRowCount(200)
        self.tb_Repos.setColumnCount(7)
        self.tb_Repos.setHorizontalHeaderLabels(
            ['REPO NAME', 'INIT', 'ADD', 'COMMIT', 'REMOTE', 'PUSH', 'REMOTE', 'REPO?'])
        # self.tb_Repos.horizontalHeaderItem().setTextAlignment(QtCore.Qt.AlignHCenter)
        # self.tb_Repos.setItem(0, 0, QTableWidgetItem("FOLDER"))
        # self.tb_Repos.setItem(0, 1, QTableWidgetItem("INIT"))
        # self.tb_Repos.setItem(0, 2, QTableWidgetItem("ADD"))
        # self.tb_Repos.setItem(0, 3, QTableWidgetItem("COMMIT"))
        # self.tb_Repos.setItem(0, 4, QTableWidgetItem("REMOTE"))
        # self.tb_Repos.setItem(0, 5, QTableWidgetItem("PUSH"))
        # self.tb_Repos.setItem(0, 6, QTableWidgetItem("REMOTE REPO?"))
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
        self.log.debug("Received signal from signum: {} with frame:{}".format(signum, frame))
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

    def monitor_set(self, selected_screen, window):
        """creates list of available monitors and moves window to
        monitor selected
        :rtype: object
        """
        screens_available = QDesktopWidget().screenCount()
        primary_screen = QDesktopWidget().primaryScreen()
        monitor = QDesktopWidget().screenGeometry(selected_screen)
        monitor_width = monitor.width()
        monitor_height = monitor.height()
        window_width = self.geometry().width()
        window_height = self.geometry().height()
        left = (monitor_width - window_width) / 2
        top = (monitor_height - window_height) / 2
        window.move(monitor.left() + left, monitor.top() + top)
        self.log.debug("Screens Available:{}  Primary Screen:{}".format(screens_available, primary_screen))
