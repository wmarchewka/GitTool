import git
from logger import Logger
import subprocess
import os
from PySide2.QtWidgets import QTableWidgetItem

PIPE = subprocess.PIPE


class GitCommands(object):

    def __init__(self, main, gui, folder_commands, data):
        self.repository = None
        self.log = Logger().log
        self.gui = gui
        self.main = main
        self.folder_commands = folder_commands
        self.data = data

    def create_remote(self, name, url):
        remote_list = self.repository.remotes
        if not remote_list:
            try:
                remote = self.repository.create_remote(name=name, remote=url)
                self.log.info(remote)
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
            self.repository.delete_remote(self.origin)
            remote = self.repository.create_remote(name=name, remote=url)
            self.log.info(remote)
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
        self.log.info("Delete Local Git:{}".format(value))

    def delete_all_git_local(self):
        row_counter = 0
        for folder in self.data.top_level_folders:
            row_counter = row_counter + 1
            self.delete_local_git(folder)

    def init(self, path, row):
        self.repository = None
        self.repository = git.Repo.init(path)
        if self.repository:
            msg = "Success"
            self.repo_config_reader()
            return True
        else:
            msg = "Failure"
            return False

    def init_check(self, path):
        self.log.info("Check for GIT folder:{}".format(path))
        try:
            _ = git.Repo(path).git_dir
            return True, 'Success'
        except git.exc.InvalidGitRepositoryError:
            return False, 'Failed'

    def add_check(self, path):
        self.log.info("Check for Files added:{}".format(path))
        try:
            status = git.Repo(path).git.status()
            sf = status.count('new file')
            if sf == 0:
                return False, "None"
            elif sf > 0:
                return True, sf
        except Exception as e:
            self.log.critial(e)
            return False

    def repo_config_reader(self):
        cr = self.repository.config_reader()
        for config in cr:
            self.log.info("Config:{}".format(config))

    def add(self, path, row):
        try:
            repo = git.Repo(path)
            repo.git.add(all=True)
        except Exception as e:
            msg = "Error adding files to .GIT"
            self.log.critical(msg)
            value = "ERROR"
            self.show_error_message(msg)
        else:
            value = "SUCCESS"
            status = repo.git.status()
            self.log.info(status)

    def commit(self, path, row):
        repo = git.Repo(path)
        # results = repo.commit()
        results = False
        if not results:
            try:
                repo.git.commit(m='Initial commit')
            except Exception as e:
                self.log.critical(e)
                msg = "Error committing files to .GIT"
                value = "ERROR"
                self.log.critical(msg)
                self.show_error_message(msg)
            else:
                value = "SUCCESS"
                status = repo.git.status()
                self.log.info(status)
                self.gui.table_widget.setItem(row, 3, QTableWidgetItem(value))
        else:
            tree = results.tree
            message = results.message
            number_of_items = len(tree)
            self.log.info("Already Commited  Length:{}   Message:{}".format(number_of_items, message))

    def commit_check(self):
        pass

    def show(self, folder, row_counter):
        # status = self.repository.git.status()
        # self.log.info(status)
        pass

    def push(self, folder, row_counter):
        # git push --set-upstream git@gitlab.example.com:namespace/nonexistent-project.git master
        try:
            for branch in self.repository.branches:
                self.log.info(branch)
            self.list_head()
            self.repository.git.push()
        except Exception as error:
            self.log.critical("ERROR PUSHING : {}".format(error))
            value = "ERROR"
        else:
            value = "Success"
        self.gui.tb_Repos.setItem(row_counter, 5, QTableWidgetItem(value))

    def list_head(self):
        head = self.repository.heads[0]
        self.log.info("Head:{}".format(head))

    def show_error_message(self, msg):
        self.log.info('Error message'.format(msg))

    def delete_selected_local_git(self, vertical_row_selected, path):
        self.log.item("Delete selected local git:{}".format(vertical_row_selected))
        path = self.data.top_level_folders[vertical_row_selected + 1]
        self.delete_local_git(path)
        self.folder_commands.get_folder_list()
