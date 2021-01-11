from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2 import QtGui
import os
import sys
import subprocess
import queue
from logger import Logger
from gui import MainWindow
from threading import Thread
import logging
import gitlab
import shutil
import git
import stat
import platform


PIPE = subprocess.PIPE


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class GitTools(object):
    def __init__(self):
        self.logger = Logger()
        os_name = platform.system()
        self.log = self.logger.log
        if os_name == 'Windows':
            self.top_level_path = r"c:\Users\z0043s5r\Desktop\GITLAB"
        elif os.name == 'Darwin':
            self.top_level_path = r"/Users/waltermarchewka/Desktop/GITLAB"
        self.top_level_folders = []
        self.top_level_filenames = []
        self.log_queue = None
        self.color_purple = QtGui.QColor("purple")
        self.color_green = QtGui.QColor("green")
        self.color_red = QtGui.QColor("red")
        self.color_yellow = QtGui.QColor("yellow")
        self.horizontal_column_selected = None
        self.vertical_row_selected = None
        self.commit_message = None
        self.queue_handler = None
        self.add_folders_to_remote_thread = None
        self.gitlab_connection = None
        self.selected_item = None
        self.gitlab_key = None
        self.window = None
        self.startup_actions()

    def startup_actions(self):
        self.log.info('Startup actions')
        self.gitlab_key = self.get_env_variable('GITLABKEY')
        self.gitlab_create_connection(self.gitlab_key)
        self.window = MainWindow()
        self.window.show()
        self.signals_and_slots()
        self.get_folder_list(self.top_level_path)
        self.gitlab_list_all_projects()
        #self.set_up_log_screen()

    def get_env_variable(self, variable):
        result = os.environ.get(variable)
        self.log.info("Get ENV Variable:{}".format(variable))
        result = "CSC-L6_1YCs8kzvHxVETtDnt"
        return result

    def gitlab_create_connection(self, private_token):
        try:
            #self.gitlab_connection = gitlab.Gitlab('https://gitlab.com/', private_token='{}'.format(private_token))
            self.gitlab_connection = gitlab.Gitlab('https://code.siemens.com/', private_token='{}'.format(private_token))
        except Exception as e:
            self.log.critical("Exception creating GITLAB connection:{}".format(e))
            return False
        else:
            return True

    def signals_and_slots(self):
        self.window.add_all_to_remote.clicked.connect(self.add_all_to_remote_clicked)
        self.window.table_widget.cellClicked.connect(self.table_clicked)
        self.window.table_widget.horizontalHeader().sectionClicked.connect(self.horizontal_header_clicked)
        self.window.table_widget.verticalHeader().sectionClicked.connect(self.vertical_header_clicked)
        self.window.delete_all_git_local.clicked.connect(self.delete_all_git_local)
        self.window.delete_selected_local_git.clicked.connect(self.delete_selected_local_git)

    def add_all_to_remote_clicked(self):
        self.add_folders_to_remote_thread = Thread(target=self.add_folders_to_remote)
        self.add_folders_to_remote_thread.start()

    def set_up_log_screen(self):
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)-9s - Module:%(module)-30s  '
            'Function:%(funcName)-30s  Line Number:%(lineno)-8d - %(message)s')
        self.queue_handler.setFormatter(formatter)
        self.logger.log.addHandler(self.queue_handler)

    def horizontal_header_clicked(self, index):
        self.log.info("Horizontal index:{}".format(index))
        self.horizontal_column_selected = index

    def vertical_header_clicked(self, index):
        self.log.info("Vertical index:{}".format(index))
        self.vertical_row_selected = index

    def table_clicked(self, row, column):
        self.log.info("TABLE CLICKED:  ROW: {}  COL: {}".format(row, column))
        self.selected_item = row, column

    def delete_remote_repository(self, repository_name):
        self.log.info("Deleting:{}".format(repository_name))

    def get_folder_list(self, path):
        row_counter = 0
        filenames = os.listdir(path)
        for filename in filenames:  # loop through all the files and folders
            filename_lowercase = self.to_lowercase(filename)
            full_path = os.path.join(self.top_level_path, filename_lowercase)
            if os.path.isdir(full_path):
                self.top_level_folders.append(full_path)
                self.top_level_filenames.append(filename_lowercase)
        self.top_level_folders.sort()
        self.top_level_filenames.sort()
        for filename in self.top_level_filenames:
            row_counter = row_counter + 1
            self.window.table_widget.setItem(row_counter, 0, QTableWidgetItem(filename))
            if self.check_for_git_folder(self.top_level_folders[row_counter - 1]):
                self.window.tableWidget.item(row_counter, 0).setBackground(self.color_green)
            else:
                self.window.tableWidget.item(row_counter, 0).setBackground(self.color_red)
            # self.window.tableWidget.item(row_counter, 0).setBackground(self.color_red)

    def check_for_git_folder(self, path):
        #self.log.info("Check for GIT folder:{}".format(path))
        process = subprocess.Popen(["git", "status", "-u", "no"], cwd=path, stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        #self.log.info("STATUS:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            msg = "ERROR this is NOT a .git repository"
            #self.log.info(msg)
            return False
        else:
            msg = "SUCCESS this is a .git repository"
            #self.log.info(msg)
            return True

    @staticmethod
    def to_lowercase(name):
        lower_name = name.lower()
        return lower_name

    def add_folders_to_remote(self):
        self.window.table_widget.clearContents()
        self.window.table_setup()
        all_record = ""
        row_counter = 0
        self.log.info("Folders:{}".format(self.top_level_folders))
        for folder in self.top_level_folders:
            row_counter = row_counter + 1
            self.log.info("Folder:{}".format(folder))
            self.init(folder=folder, row_counter=row_counter)
            self.add(folder=folder, row_counter=row_counter)
            self.commit(folder=folder, row_counter=row_counter)
            self.show(folder=folder, row_counter=row_counter)
            self.push(folder=folder, row_counter=row_counter, lowercase_folder=folder)
            record = self.log_queue.get(block=False)
            if record is not None:
                all_record = all_record + str(record)
                self.window.plainTextEdit.insertPlainText(str(record) + '\r\n\n')

    def delete_selected_local_git(self, path):
        self.log.item("Delete selected local git:{}".format(self.vertical_row_selected))
        path = self.top_level_folders[self.vertical_row_selected + 1]
        self.delete_local_git(path)
        self.get_folder_list(self.top_level_path)

    def delete_local_git(self, path):
        print(os.getcwd())
        #path = path + "/.git"
        process = subprocess.Popen(["git", "rm", "-r", path], stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        self.log.info("INIT:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            value = "ERROR : "
        else:
            value = "SUCCESS : "

    def delete_all_git_local(self):
        row_counter = 0
        for folder in self.top_level_folders:
            row_counter = row_counter + 1
            self.delete_local_git(folder)

    def init(self, folder, row_counter):
        process = subprocess.Popen(["git", "init"], cwd=folder, stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        self.log.info("INIT:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            value = "ERROR : "
        else:
            value = "SUCCESS : "
        if stdoutput.find(b'Reinitialized') != -1:
            value = value + "RE-INIT"
            self.commit_message = f'{"Changes"}'
        if stdoutput.find(b'Reinitialized') == -1:
            self.commit_message = f'{"Initial commit"}'
        self.window.table_widget.setItem(row_counter, 1, QTableWidgetItem(value))

    def add(self, folder, row_counter):
        process = subprocess.Popen(["git", "add", "."], cwd=folder, stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        self.log.info("ADD:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            value = "ERROR : "
        else:
            value = "SUCCESS : "
        self.window.table_widget.setItem(row_counter, 2, QTableWidgetItem(value))

    def commit(self, folder, row_counter):
        process = subprocess.Popen(["git", "commit", "-m", self.commit_message], cwd=folder, stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        self.log.info("COMMIT:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            value = "ERROR : "
        else:
            value = "SUCCESS : "
        # if stdoutput.find(b'Nothing to commit') != -1:
        #value = value + str(stdoutput)
        self.window.table_widget.setItem(row_counter, 3, QTableWidgetItem(value))

    def show(self, folder, row_counter):
        process = subprocess.Popen(["git", "show"], cwd=folder, stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        self.log.info("SHOW:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            value = "ERROR : "
        else:
            value = "SUCCESS : "
        # if stdoutput.find(b'Nothing to commit') != -1:
        # value = value + str(stdoutput)
        self.window.table_widget.setItem(row_counter, 4, QTableWidgetItem(value))

    def push(self, folder, row_counter, lowercase_folder):
        # git push --set-upstream git@gitlab.example.com:namespace/nonexistent-project.git master
        command = r'git@code.siemens.com:walter.marchewka/' + lowercase_folder + '.git'
        self.log.info("PUSH:{}".format(command))
        process = subprocess.Popen(["git", "push", "--set-upstream", command, "master"], cwd=folder, stdout=PIPE,
                                   stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        self.log.info("SHOW:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            value = "ERROR : "
        else:
            value = "SUCCESS : "
            # if stdoutput.find(b'Nothing to commit') != -1:
        #value = value + str(stdoutput)
        self.window.table_widget.setItem(row_counter, 5, QTableWidgetItem(value))

    def gitlab_delete(self, id):
        try:
            status = self.gitlab_connection.projects.delete(id)
            print(status)
        except gitlab.exceptions.GitlabDeleteError:
            print('File not found"')

    def gitlab_list_all_projects(self):
        remote_projects = self.gitlab_connection.projects.list(owned=True)
        value = None
        row_counter = 0
        for local_project_name in self.top_level_filenames:
            for project in [project for project in (remote_projects or [])]:
            #for project in remote_projects:
                remote_project_name = project.name
                remote_project_id = project.id
                self.log.info("Project Name:{}   ID:{}".format(remote_project_name, remote_project_id))
                row_counter = row_counter + 1
                if local_project_name == remote_project_name:
                    value = "YES"
                else:
                    value = "NO"
                self.window.table_widget.setItem(row_counter, 6, QTableWidgetItem(value))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    gT = GitTools()
    app.exec_()
