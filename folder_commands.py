from logger import Logger
import os
import subprocess

PIPE = subprocess.PIPE


class FolderCommands(object):

    def __init__(self, main, gui, data):
        self.log = Logger().log
        self.horizontal_column_selected = None
        self.vertical_row_selected = None
        self.selected_item = None
        self.gui = gui
        self.data = data
        self.main = main
        # self.gitlab_commands = main.gitCommands
        # self.git_commands = main.gitLabCommands

    def get_folder_list(self):
        top_level_path = self.data.top_level_path
        self.data.top_level_folders = []
        self.data.top_level_filenames = []
        if top_level_path is not None:
            row_counter = 0
            filenames = os.listdir(top_level_path)
            for filename in filenames:  # loop through all the files and folders
                filename_lowercase = self.to_lowercase(filename)
                full_path = os.path.join(top_level_path, filename_lowercase)
                if os.path.isdir(full_path):
                    self.data.top_level_folders.append(full_path)
                    self.data.top_level_filenames.append(filename_lowercase)
            self.data.top_level_folders.sort()
            self.data.top_level_filenames.sort()
        else:
            self.show_error_message("Please select local Path")

    def startup_check(self):
        row_counter = 0
        for filename in self.data.top_level_filenames:
            row_counter = row_counter + 1
            self.gui.table_set_item_text(row=row_counter, column=0, text=filename)
            self.init_check(row_counter)
            self.add_check(row_counter)

    def init_check(self, row_counter):
        result, msg = self.main.gitCommands.init_check(self.data.top_level_folders[row_counter - 1])
        if result:
            self.gui.table_set_item_text(row_counter, 1, str(msg))
            self.gui.table_set_item_background(row_counter, 1, 'green')
        else:
            self.gui.table_set_item_text(row_counter, 1, str(msg))
            self.gui.table_set_item_background(row_counter, 1, 'red')

    def add_check(self, row_counter):
        result, msg = self.main.gitCommands.add_check(self.data.top_level_folders[row_counter - 1])
        if result:
            self.gui.table_set_item_text(row_counter, 2, str(msg))
            self.gui.table_set_item_background(row_counter, 2, 'green')
        else:
            self.gui.table_set_item_text(row_counter, 2, str(msg))
            self.gui.table_set_item_background(row_counter, 2, 'red')

    def add_folders_to_remote(self):
        self.gui.tb_Repos.clearContents()
        self.gui.table_setup()
        all_record = ""
        row_counter = 0
        self.log.info("Folders:{}".format(self.data.top_level_folders))
        for folder in self.data.top_level_folders:
            row_counter = row_counter + 1
            self.log.info("Folder:{}".format(folder))
            self.main.git_commands.init(folder=folder, row_counter=row_counter)
            self.main.git_commands.add(folder=folder, row_counter=row_counter)
            self.main.git_commands.commit(folder=folder, row_counter=row_counter)
            self.main.git_commands.show(folder=folder, row_counter=row_counter)
            self.main.git_commands_push(folder=folder, row_counter=row_counter, lowercase_folder=folder)

    def add_all_to_remote_clicked(self):
        self.add_folders_to_remote()

    @staticmethod
    def to_lowercase(name):
        lower_name = name.lower()
        return lower_name

    def show_error_message(self, msg):
        self.log.info("Show error message: {}".format(msg))
