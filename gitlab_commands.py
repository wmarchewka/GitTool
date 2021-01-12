from logger import Logger
import gitlab


class GitLabCommands(object):

    def __init__(self, window):
        self.log = Logger().log
        self.window = window

    def gitlab_create_connection(self, url, private_token):
        if url is not None and private_token is not None:
            self.log.info("Creating connection")
            try:
                self.gitlab_connection = gitlab.Gitlab(url, private_token='{}'.format(private_token))
                self.log.info("Setting url:{}".format(url))
            except Exception as e:
                self.log.critical("Exception creating GITLAB connection:{}".format(e))
                self.show_error_message("Error Creating Connection")
                return False
            else:
                self.log.info("Successfully created connection")
        else:
            msg = ""
            if url is None:
                msg = "Url is blank"
            if private_token is None:
                msg = msg + '\r\n' + "Token is blank"
            self.show_error_message(msg)
            return False

    def create_connection_pressed(self):
        url, token = self.get_connection_info()
        self.gitlab_create_connection(url=url, private_token=token)

    def show_error_message(self, msg):
        self.log.info("Show error message: {}".format(msg))

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
                # for project in remote_projects:
                remote_project_name = project.name
                remote_project_id = project.id
                self.log.info("Project Name:{}   ID:{}".format(remote_project_name, remote_project_id))
                row_counter = row_counter + 1
                if local_project_name == remote_project_name:
                    value = "YES"
                else:
                    value = "NO"
                self.window.table_widget.setItem(row_counter, 6, QTableWidgetItem(value))
