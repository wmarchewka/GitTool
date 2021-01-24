from logger import Logger
import gitlab


class GitLabCommands(object):

    def __init__(self, main, gui, folder_commands, data):
        self.log = Logger().log
        self.gui = gui
        self.main = main
        self.folder_commands = folder_commands
        self.data = data
        self.connection_made = False
        self.gitlab_connection = None

    def create_connection(self):
        if self.connection_made is not True:
            url = self.data.url
            url = self.data.gitlab_api_url
            private_token = self.data.token
            if url is not None and private_token is not None:
                self.log.info("Creating connection")
                try:
                    self.gitlab_connection = gitlab.Gitlab(url, private_token='{}'.format(private_token))
                    self.log.info("Setting url:{}".format(url))
                except Exception as e:
                    self.log.critical("Exception creating GITLAB connection:{}".format(e))
                    self.show_error_message("Error Creating Connection")
                    self.connection_made = False
                    return False
                else:
                    self.log.info("Successfully created connection")
                    self.connection_made = True
                    return True
            else:
                msg = ""
                if url is None:
                    msg = "Url is blank"
                if private_token is None:
                    msg = msg + '\r\n' + "Token is blank"
                self.show_error_message(msg)
                return False
        return True

    def create_connection_pressed(self):
        pass
        # url, token = self.get_connection_info()
        # self.gitlab_create_connection(url=url, private_token=token)

    def repo_check(self, path):
        self.log.debug("Gitlab repo check  PATH:{}".format(path))
        name = self.main.folderCommands.pathname_to_filename(path)
        if self.create_connection():
            project_list = self.gitlab_connection.projects.list(owned=True, search=name)
            self.log.debug("Getting project on GITLAB:  PROJECT:{}".format(name))
            index = self.index_from_project_list(project_list=project_list, search_name=name)
            if le(project_list):
                if index is not None:
                    project = project_list[index]
                    project_id = project.id
                    self.log.debug("Found project on remote repo")
                    return True, project_id
                else:
                    return False, "NONE"
            else:
                self.log.debug('did not find remote repo')
                return False, "NONE"

    def delete_remote_git(self, path):
        self.log.debug("Gitlab repo check  PATH:{}".format(path))
        name = self.main.folderCommands.pathname_to_filename(path)
        if self.create_connection():
            project_list = self.gitlab_connection.projects.list(owned=True, search=name)
            self.log.debug("Getting project on GITLAB:  PROJECT:{}".format(name))
            index = self.index_from_project_list(project_list=project_list, search_name=name)
            if le(project_list):
                if index is not None:
                    project = project_list[index]
                    project_id = project.id
                    if self._gitlab_delete(project_id):
                        return True, project_id
                    else:
                        return False, "Error deleting"
                else:
                    return False, "Error finding"
            else:
                return False, "NONE"

    def index_from_project_list(self, project_list, search_name):
        counter = 0
        for project in project_list:
            name = project.name
            id = project.id
            if search_name == name:
                return counter
            else:
                counter = counter + 1
        return None

    def show_error_message(self, msg):
        self.log.info("Show error message: {}".format(msg))

    def _gitlab_delete(self, project_id):
        try:
            status = self.gitlab_connection.projects.delete(project_id)
            self.log.debug(status)
            return True
        except gitlab.exceptions.GitlabDeleteError:
            self.log.debug('File not found"')
            return False

    def gitlab_list_all_projects(self, top_level_filenames):
        remote_projects = self.gitlab_connection.projects.list(owned=True)
        value = None
        row_counter = 0
        for local_project_name in top_level_filenames:
            for project in [project for project in (remote_projects or [])]:
                # for project in remote_projects:
                remote_project_name = project.name
                remote_project_id = project.id
                self.log.info("Project Name:{}   ID:{}".format(remote_project_name, remote_project_id))
                row_counter = row_counter + 1
                if local_project_name == remote_project_name:
                    value = "YES"
                else:
                    value = "NO"
                self.gui.set_item_text(row_counter, 6, value)

    def get_projects_list(self):
        self.create_connection()
        remote_projects = self.gitlab_connection.projects.list(owned=True)
        return remote_projects

    def delete_remote_repository(self, repository_name):
        self.log.info("Deleting:{}".format(repository_name))

    # url, token = self.get_connection_info()
    # if self.gitlab_create_connection(url=url, private_token=token):


def le(list1):
    if len(list1) == 0:
        return 0
    else:
        return 1
