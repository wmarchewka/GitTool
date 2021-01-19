from PySide2.QtWidgets import QApplication, QMessageBox
# import os
# import platform
import sys
from logger import Logger
from gui import MainWindow
from git_commands import GitCommands
from gitlab_commands import GitLabCommands
from folder_commands import FolderCommands
from data import Data
import threading

class BteTools(object):
    def __init__(self):
        self.logger = Logger()
        # os_name = platform.system()
        self.log = self.logger.log
        self.data = Data()
        self.gui = MainWindow(main=self, data=self.data)
        self.folderCommands = FolderCommands(main=self, gui=self.gui, data=self.data)
        self.gitCommands = GitCommands(main=self, gui=self.gui, folder_commands=self.folderCommands, data=self.data)
        self.gitLabCommands = GitLabCommands(main=self, gui=self.gui, folder_commands=self.folderCommands,
                                             data=self.data)
        self.startup_actions()

    def startup_actions(self):
        self.log.info('Startup actions')
        # self.gitlab_key = self.get_env_variable('GITLABKEY')
        self.populate_screen()
        self.gui.show()
        # self.gui.pb_get_local_folders_clicked()
        # get_folders_thread = threading.Thread(target = )
        # get_folders_thread.start()

    @staticmethod
    def show_error_message(error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_message)
        msg.setInformativeText('More information')
        msg.setWindowTitle("Error")
        msg.exec_()

    def populate_screen(self):
        self.gui.rb_siemens_url.setText(self.data.siemens_txt_url)
        self.gui.rb_gitlab_url.setText(self.data.gitlab_txt_url)
        self.gui.rb_gitlab_url.setChecked(True)

    def get_env_variable(self, variable):
        # env_var = os.environ.get(variable)
        self.log.info("Get ENV Variable:{}".format(variable))
        env_var = "CSC-L6_1YCs8kzvHxVETtDnt"
        return env_var


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bte = BteTools()
    app.exec_()
