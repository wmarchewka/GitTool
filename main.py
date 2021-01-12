from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
import os
import sys
import platform
from pathlib import Path

from logger import Logger
from gui import MainWindow
from git_commands import GitCommands
from gitlab_commands import GitLabCommands
from folder_commands import FolderCommands


class BTE_Tools(object):
    def __init__(self):
        self.logger = Logger()
        os_name = platform.system()
        self.log = self.logger.log
        self.gui = MainWindow()
        self.gitCommands = GitCommands(self.gui)
        self.gitLabCommands = GitLabCommands(self.gui)
        self.folderCommands = FolderCommands(self.gui)
        self.top_level_path = '/Users/waltermarchewka/Desktop/GITLAB'
        self.siemens_txt_url = '://code.siemens.com/'
        self.gitlab_txt_url = 'git@gitlab.com/siemensbte'
        self.origin = 'origin'
        self.top_level_folders = []
        self.top_level_filenames = []
        self.commit_message = None
        self.gitlab_connection = None
        self.gitlab_key = None
        self.remote = None
        self.new_repository = None
        self.selected_token = None
        self.startup_actions()

    def startup_actions(self):
        self.log.info('Startup actions')
        # self.gitlab_key = self.get_env_variable('GITLABKEY')
        self.populate_screen()
        self.gui.window.show()

    def show_error_message(self, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_message)
        msg.setInformativeText('More information')
        msg.setWindowTitle("Error")
        msg.exec_()

    def populate_screen(self):
        self.gui.siemens_url.setText(self.siemens_txt_url)
        self.gui.rb_gitlab_url.setText(self.gitlab_txt_url)
        self.gui.rb_gitlab_url.setChecked(True)
        self.gui.window.te_local_path.setText(self.top_level_path)
        self.gui.te_token.setText('zX3Sz3_-3XadLdHqD_tR')

    def get_env_variable(self, variable):
        result = os.environ.get(variable)
        self.log.info("Get ENV Variable:{}".format(variable))
        result = "CSC-L6_1YCs8kzvHxVETtDnt"
        return result

    def delete_remote_repository(self, repository_name):
        self.log.info("Deleting:{}".format(repository_name))

    def delete_selected_local_git(self, path):
        self.log.item("Delete selected local git:{}".format(self.vertical_row_selected))
        path = self.top_level_folders[self.vertical_row_selected + 1]
        self.delete_local_git(path)
        self.get_folder_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bte = BTE_Tools()
    app.exec_()
