import git
from logger import Logger
import subprocess
import os
import time
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
        self.log.debug("git Create remote  NAME{}   URL:{}".format(name, url))
        remote_list = self.repository.remotes
        if not remote_list:
            try:
                remote = self.repository.create_remote(name=name, remote=url)
                self.log.debug(remote)
                return True
            except git.exc.GitCommandError as error:
                msg = f'Error creating remote: {error}'
                self.log.debug(msg)
                self.show_error_message(msg)
                return False
        else:
            self.log.debug("Remote exists !!!")
            for remote in remote_list:
                self.log.debug(("Remote: Name:{}    Url:{}".format(remote.name, remote.url)))
            self.repository.delete_remote(self.origin)
            remote = self.repository.create_remote(name=name, remote=url)
            self.log.debug(remote)
            return True

    def delete_local_git(self, path):
        self.log.debug("git delete local folder  ROW:{}".format(path))
        print(os.getcwd())
        # path = path + "/.git"
        process = subprocess.Popen(["git", "rm", "-r", path], stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        self.log.debug("INIT:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            value = "ERROR : "
        else:
            value = "SUCCESS : "
        self.log.debug("Delete Local Git:{}".format(value))

    def delete_all_git_local(self):
        row_counter = 0
        for folder in self.data.top_level_folders:
            row_counter = row_counter + 1
            self.delete_local_git(folder)

    def init(self, path, row):
        self.log.debug("git PUSH  PATH:{}   ROW:{}".format(path, row))
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
        self.log.debug("init check GIT folder:{}".format(path))
        try:
            _ = git.Repo(path).git_dir
            return True, 'Success'
        except git.exc.InvalidGitRepositoryError:
            return False, 'None'

    def add_check(self, path):
        self.log.debug("GIT ADD check added:{}".format(path))
        try:
            status = git.Repo(path).git.status()
            sf = status.count('new file')
            if sf == 0:
                return False, "None"
            elif sf > 0:
                return True, sf
        except Exception as e:
            self.log.debug(e)
            return False, "None"

    def repo_config_reader(self):
        self.log.debug("git  REPO CONFIG reader".format())
        cr = self.repository.config_reader()
        for config in cr:
            self.log.debug("Config:{}".format(config))

    def add(self, path, row):
        self.log.debug("git ADD  PATH:{}   ROW:{}".format(path, row))
        try:
            repo = git.Repo(path)
            repo.git.add(all=True)
        except Exception as e:
            msg = "Error adding files to .GIT"
            self.log.debug(msg)
            value = "ERROR"
            self.show_error_message(msg)
        else:
            value = "SUCCESS"
            status = repo.git.status()
            self.log.debug("GIT STATUS :{}".format(status))

    def commit(self, path, row):
        self.log.debug("git COMMIT  PATH:{}   ROW:{}".format(path, row))
        repo = git.Repo(path)
        results = False
        if not results:
            try:
                repo.git.commit(m='Initial commit')
            except Exception as e:
                self.log.debug(e)
                msg = "Error committing files to .GIT"
                value = "ERROR"
                self.log.debug(msg)
                self.show_error_message(msg)
            else:
                value = "SUCCESS"
                status = repo.git.status()
                self.log.debug(status)
                self.gui.tb_Repos.setItem(row, 3, QTableWidgetItem(value))
        else:
            tree = results.tree
            message = results.message
            number_of_items = len(tree)
            self.log.debug("Already Commited  Length:{}   Message:{}".format(number_of_items, message))

    def commit_check(self, path):
        self.log.debug("git COMMIT check PATH:{}".format(path))
        try:
            repo = git.Repo(path)
            commit = repo.commit()
            commit_date = commit.committed_date
        except Exception as e:
            self.log.debug("COMMIT check ERROR:{}".format(e))
            return False, "No Commit"
        else:
            self.log.debug("Commit files:{}".format(commit_date))
            if commit_date:
                self.log.debug("COMMIT found Date:{}".format(commit_date))
                # time.asctime(time.gmtime(commit_date))
                gmt = time.gmtime(commit_date)
                str_time = time.strftime("%a, %d %b %Y %H:%M", gmt)
                return True, str_time
            else:
                return False, "None"

    def show(self, folder, row_counter):
        # status = self.repository.git.status()
        # self.log.debug(status)
        pass

    def remote(self, path, row):
        self.log.debug("git REMOTE CREATE  PATH:{}   ROW:{}".format(path, row))
        repo = git.Repo(path)
        name = self.data.top_level_filenames[row]
        url = self.data.url + '/' + name
        self.log.debug("Creating REMOTE with NAME:{}   URL:{}".format(name, url))
        try:
            origin = repo.create_remote(name, url)
            repo.heads.master.set_tracking_branch(origin.refs.master)
        except git.exc.GitCommandError as error:
            self.log.debug("ERROR REMOTE EXISTS")
            remotes = repo.remotes
            self.log.debug('REMOTES :{}'.format(remotes))

    def config(self, key):
        config = git.config_reader()
        path = config.get_config_path

        self.log.info("CONFIG  PATH:{}".format(path))

    def remote_check(self, path):
        self.log.debug("git REMOTE check  PATH:{}".format(path))
        try:
            repo = git.Repo(path)
            remotes = repo.remotes
            self.log.debug('REMOTES :{}'.format(remotes))
            if remotes:
                return True, remotes
            else:
                return False, "None"
        except git.exc.InvalidGitRepositoryError:
            self.log.debug("No REPO")
            return False, "None"

    def push(self, path, row):
        self.log.debug("git PUSH  ROW:{}".format(row))
        # git push --set-upstream git@gitlab.example.com:namespace/nonexistent-project.git master
        repo = git.Repo(path)
        remote = repo.remotes[0]
        self.config(None)
        self.remote_attributes(repo=repo)
        self.log.info('Remote url:{}'.format(remote.url))
        self.log.info("REMOTE:{}".format(remote))
        try:
            remote.push()
        except Exception as error:
            self.log.info("ERROR PUSHING : {}".format(error))
            value = "ERROR"
        else:
            value = "Success"
        self.gui.tb_Repos.setItem(row, 5, QTableWidgetItem(value))

    def remote_attributes(self, repo):
        reader = repo.config_reader()
        # reader.get_value()
        # self.log.info(reader)

    def list_head(self, repo, path):
        self.log.debug("git LIST HEAD  PATH:{}".format(path))
        head = repo.heads[0]
        self.log.debug("Head:{}".format(head))

    def show_error_message(self, msg):
        self.log.debug('Error message'.format(msg))

    def delete_selected_local_git(self, vertical_row_selected, path):
        self.log.item("Delete selected local git:{}".format(vertical_row_selected))
        path = self.data.top_level_folders[vertical_row_selected + 1]
        self.delete_local_git(path)
        self.folder_commands.get_folder_list()
