import git
from logger import Logger
import subprocess
import os
from PySide2.QtWidgets import QTableWidgetItem

PIPE = subprocess.PIPE


class GitCommands(object):

    def __init__(self, window):
        self.repository = None
        self.log = Logger().log
        self.window = window
        self.top_level_folders = None

    def create_remote(self, name, url):
        remote_list = self.repository.remotes
        if not remote_list:
            try:
                remote = self.repository.create_remote(name=name, remote=url)
                return True
            except git.exc.GitCommandError as error:
                msg = f'Error creating remote: {error}'
                self.log.critical(msg)
                self.show_error_message(msg)
                return False
        else:
            self.log.info("Remote exists !!!")
            for remote in remote_list:
                self.log.info(("Remote: Name:{}    Url:{}".format(remote.name, remote.url)))
            self.repository.delete_remote(origin)
            remote = self.repository.create_remote(name=name, remote=url)
            return True

    def delete_local_git(self, path):
        print(os.getcwd())
        # path = path + "/.git"
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
        self.repository = None
        self.repository = git.Repo.init(folder)
        if self.repository:
            msg = "Success"
            self.repo_config_reader()
        else:
            msg = "Failure"
        self.window.table_widget.setItem(row_counter, 1, QTableWidgetItem("Success"))

    def repo_config_reader(self):
        cr = self.repository.config_reader()
        for config in cr:
            self.log.info("Config:{}".format(config))

    def add(self, folder, row_counter):
        try:
            self.repository.git.add(all=True)
        except Exception as e:
            msg = "Error adding files to .GIT"
            self.log.critical(msg)
            value = "ERROR"
            self.show_error_message(msg)
        else:
            value = "SUCCESS"
            status = self.repository.git.status()
            self.log.info(status)
        self.window.table_widget.setItem(row_counter, 2, QTableWidgetItem(value))

    def commit(self, folder, row_counter):
        results = self.repository.commit()
        if not results:
            try:
                self.repository.git.commit(m='Initial commit')
            except Exception as e:
                self.log.critical(e)
                msg = "Error committing files to .GIT"
                value = "ERROR"
                self.log.critical(msg)
                self.show_error_message(msg)
            else:
                value = "SUCCESS"
                status = self.repository.git.status()
                self.log.info(status)
                self.window.table_widget.setItem(row_counter, 3, QTableWidgetItem(value))
        else:
            tree = results.tree
            message = results.message
            number_of_items = len(tree)
            self.log.info("Already Commited  Length:{}   Message:{}".format(number_of_items, message))

    def show(self, folder, row_counter):
        # status = self.repository.git.status()
        # self.log.info(status)
        pass

    def push(self, folder, row_counter, lowercase_folder):
        # git push --set-upstream git@gitlab.example.com:namespace/nonexistent-project.git master
        url, token = self.get_connection_info()
        if self.gitlab_create_connection(url=url, private_token=token):
            try:
                for branch in self.repository.branches:
                    self.log.info(branch)
                self.list_head()
                self.repository.git.push()
                value = "Success"
            except Exception as error:
                self.log.critical("ERROR PUSHING : {}".format(error))
                value = "ERROR"
        else:
            value = 'Error'
        self.window.tb_Repos.setItem(row_counter, 5, QTableWidgetItem(value))

    def list_head(self):
        head = self.repository.heads[0]
        self.log.info("Head:{}".format(head))

    def show_error_message(self, msg):
        self.log.info('Error message'.format(msg))
