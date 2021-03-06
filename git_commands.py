from logger import Logger
import subprocess
import os
import time

PIPE = subprocess.PIPE


class GitCommands(object):

    def __init__(self, main, gui, folder_commands, data):
        self.repository = None
        self.log = Logger().log
        self.gui = gui
        self.main = main
        self.folder_commands = folder_commands
        self.data = data

    def init(self, path):
        self.log.debug("git INIT  PATH:{}".format(path))
        os.chdir(path)
        try:
            result = subprocess.run(['git', 'init'], capture_output=True, text=True)
            self.log.debug("init check result:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            # noinspection PyTypeChecker
            if err.find("not a git repository") != -1:  # returns position in string where found
                return False, 'None'
            elif out.find("reinitialized existing git repository") != -1:
                return True, 'Success'
            elif out.find('reenitialized empty git repository') != -1:
                return True, 'Success'
            elif out.find('initialized empty git repository') != -1:
                return True, 'Success'
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'Not found'
            else:
                return False, 'Error'

    def add(self, path):
        self.log.debug("git ADD  PATH:{}".format(path))
        os.chdir(path)
        try:
            result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
            self.log.debug("init check result:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            return_code = result.returncode
            if return_code == 0:  # returns position in string where found
                return True, 'Success'
            else:
                return False, 'ERROR'
        except Exception as error:
            err_str = error.args[0]
            self.log.info("ADD ERROR:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'Not found'
            else:
                return False, 'Error'

    def commit(self, path):
        self.log.debug("git COMMIT  PATH:{}".format(path))
        os.chdir(path)
        try:
            result = subprocess.run(['git', 'commit', '-m', 'Initial commit'], capture_output=True, text=True)
            self.log.debug("COMMIT:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            return_code = result.returncode
            # noinspection PyTypeChecker
            if out.find("initial commit") != -1:  # returns position in string where found
                return True, 'Initial commit'
            if return_code == 0:  # returns position in string where found
                return True, 'Success'
            else:
                return False, 'ERROR'
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'Not found'
            else:
                return False, 'Error'

    def remote(self, path, name, url):
        self.log.debug("git REMOTE CREATE  PATH:{}".format(path))
        os.chdir(path)
        try:
            # git remote add origin https://github.com/user/repo.git
            result = subprocess.run(['git', 'remote', 'add', 'origin', url], capture_output=True, text=True)
            self.log.debug("COMMIT:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            return_code = result.returncode
            checked_url = self.get_remote_url(path)
            # noinspection PyTypeChecker
            if return_code == 0:  # returns position in string where found
                return True, checked_url
            elif err.find("remote origin already exists") != -1:
                return True, checked_url
            else:
                return False, 'ERROR'
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'Not found'
            else:
                return False, 'Error'

    def push(self, path):
        self.log.debug("git PUSH:{}".format(path))
        os.chdir(path)
        try:
            # git push 111 master
            # name = self.main.folderCommands.pathname_to_filename(path)
            result = subprocess.run(['git', 'push', '--set-upstream', 'origin', 'master'], capture_output=True,
                                    text=True)
            self.log.debug("PUSH:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            return_code = result.returncode
            # noinspection PyTypeChecker
            if return_code == 0:  # returns position in string where found
                return True, None
            elif err.find("remote origin already exists") != -1:
                return True, None
            elif err.find('permission denied') != -1:
                return False, 'Permission denied'
            else:
                return False, 'ERROR'

        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'Not found'
            else:
                return False, 'Error'

    def init_check(self, path):
        self.log.debug("init check GIT folder:{}".format(path))
        os.chdir(path)
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            self.log.debug("init check result:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower().lower()
            # noinspection PyTypeChecker
            if err.find("not a git repository") != -1:  # returns position in string where found
                return False, 'No repo found'
            elif out.find("on branch master") != -1:
                return True, 'Success'
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'No repo found'
            else:
                return False, 'Error'

    def add_check(self, path):
        counter = 0
        os.chdir(path)
        self.log.debug("GIT ADD check added:{}".format(path))
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            self.log.debug("init check result:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            # noinspection PyTypeChecker
            count = out.count("new file")
            # noinspection PyTypeChecker
            if err.find("not a git repository") != -1:  # returns position in string where found
                return False, 'No repo found'
            elif count > 0:
                return True, count
            elif out.find("on branch master") != -1:
                return False, "None"
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'No repo found'
            else:
                return False, 'Error'

    def commit_check(self, path):
        self.log.debug("git COMMIT check PATH:{}".format(path))
        os.chdir(path)
        try:
            result = subprocess.run(['git', 'show'], capture_output=True, text=True)
            # result = result[:256]
            # self.log.debug("init check result:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            # noinspection PyTypeChecker
            if err.find("not a git repository") != -1:  # returns position in string where found
                return False, 'No repo found'
            elif out.find("commit") != -1:
                git_date = self.get_commit_date(path)
                return True, git_date
            elif err.find("does not have any commits yet") != -1:
                return False, 'No commits'
        except UnicodeDecodeError as error:
            self.log.debug('Exception in Commit Check:{}'.format(error))
            return True, "No commits"
        except Exception as error:
            self.log.debug('Exception in Commit Check:{}'.format(error))
            return False, "ERROR"
        else:
            return False, "ERROR"

    def remote_check(self, path):
        os.chdir(path)
        self.log.debug("git REMOTE check  PATH:{}".format(path))
        try:
            remote_url = self.get_remote_url(path=path)
            if remote_url is not '':
                return True, remote_url
            else:
                return False, 'No remote repo set'
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'No repo found'
            else:
                return False, 'Error'

    def push_check(self, path):
        self.log.debug("git  PUSH CHECK  PATH:{}".format(path))
        os.chdir(path)
        try:
            # git fetch --dry-run --verbose
            result = subprocess.run(['git', 'fetch', '--dry-run', '--verbose'], capture_output=True, text=True)
            self.log.debug("PUSH CHECK result:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            return_code = result.returncode
            # noinspection PyTypeChecker
            if err.find(
                    "the project you were looking for could not be found") != -1:  # returns position in string where found
                return False, 'Missing'
            elif err.find("[new branch]") != -1:  # returns position in string where found
                return True, 'New Branch'
            elif err.find('[up to date]') != -1:
                return True, 'Up to date'
            elif err.find('not a git repository') != -1:
                return False, 'No Repo'
            elif err.find('no remote repository specified') != -1:
                return False, 'No Repo'
            elif err.find('could not read from remote repository') != -1:
                return False, 'No Repo'
            elif return_code == 0:
                return True, 'Up to date'
        except Exception as error:
            self.log.info("INIT Check error:{}".format(error))
            return False, 'ERROR'

    def config_check(self, path):
        self.log.debug("git  REPO CONFIG reader".format())
        os.chdir(path)
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            self.log.debug("init check result:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            # noinspection PyTypeChecker
            if err.find("not a git repository") != -1:  # returns position in string where found
                return False, 'None'
            else:
                return False, 'None'
        except Exception as error:
            self.log.info("INIT Check error:{}".format(error))
            return False, 'Error'

    def show_error_message(self, msg):
        self.log.debug('Error message'.format(msg))

    def delete_local_git(self, path):
        self.log.debug("git delete local folder  ROW:{}".format(path))
        self.log.debug("Local path:{}".format(os.getcwd()))
        path = path + "/.git"
        value = ""
        result = subprocess.run(['rm', '-r', path], capture_output=True, text=True)
        self.log.debug("init check result:{}".format(result))
        err = result.stderr.lower()
        out = result.stdout.lower()
        return_code = result.returncode
        self.log.debug("INIT:{}  ERROR:{}".format(out, err))
        # noinspection PyTypeChecker
        if err.find("no such file or directory") != -1:
            value = "ERROR : "
        elif return_code == 0:
            value = "SUCCESS : "
        self.log.debug("Delete Local Git:{}".format(value))

    def delete_all_git_local(self):
        row_counter = 0
        for folder in self.data.top_level_folders:
            row_counter = row_counter + 1
            self.delete_local_git(folder)

    def get_commit_date(self, path):
        os.chdir(path)
        try:
            result = subprocess.run(['git', 'log', '-1', '--format=%cd'], capture_output=True, text=True)
            self.log.debug("Get COMMIT DATE:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            # noinspection PyTypeChecker
            if err.find("not a git repository") != -1:  # returns position in string where found
                return None
            else:
                return out
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'Not found'
            else:
                return False, 'Error'

    def get_remote_url(self, path):
        os.chdir(path)
        try:
            # git config --get remote.origin.url
            result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True)
            self.log.debug("Get REMOTE URL DATE:{}".format(result))
            err = result.stderr.lower()
            out = result.stdout.lower()
            # noinspection PyTypeChecker
            if err.find("not a git repository") != -1:  # returns position in string where found
                return None
            else:
                return out
        except Exception as error:
            err_str = error.args[0]
            self.log.info("INIT Check error:{}".format(err_str))
            if err_str.find("repository not found") != -1:
                return False, 'Not found'
            else:
                return False, 'Error'

    def create_subtree(self, project):
        # git subtree add --prefix 111/ git@gitlab.com:siemensbte/drivers/111.git master --squash
        #
        value = ""
        top_level_pull_path = self.data.top_level_pull_path
        folder_for_subtree = project.name
        remote_url = self.data.url
        remote_project_name = project.name + '.git'
        remote_project = os.path.join(remote_url, remote_project_name)
        new_path = os.path.join(top_level_pull_path, folder_for_subtree)
        os.chdir(top_level_pull_path)
        result = subprocess.run(
            ['git', 'subtree', 'add', '--prefix', folder_for_subtree, remote_project, 'master', '--squash'],
            capture_output=True, text=True)
        self.log.debug("init check result:{}".format(result))
        err = result.stderr.lower()
        out = result.stdout.lower()
        return_code = result.returncode

        self.log.debug("INIT:{}  ERROR:{}".format(out, err))
        # noinspection PyTypeChecker
        if err.find("no common commits") != -1:
            value = "SUCCESS : "
            return True, new_path
        elif return_code == 0:
            value = "SUCCESS : "
            return True, new_path
        else:
            return False, "ERROR"

    def create_readme(self, path):
        os.chdir(path)
        f = open("READ.me", "x")
        f.write("README")
        f.close()
