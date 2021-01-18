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

    def get_folder_list(self):
        self.log.debug("Getting folder list")
        top_level_path = self.data.top_level_path
        self.data.top_level_folders = []
        self.data.top_level_filenames = []
        if top_level_path is not None:
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

    def check_all_folders(self):
        self.log.debug("Startup check")
        row_counter = 0
        for filename in self.data.top_level_filenames:
            self.check_one_folder(row=row_counter, filename=filename)
            row_counter = row_counter + 1

    def check_one_folder(self, row, filename):
        self.gui.table_set_item_text(row=row, column=0, text=filename)
        self.perform_check(row)

    def perform_check(self, row):
        self.init_check(row)
        self.add_check(row)
        self.commit_check(row)
        self.remote_check(row)
        self.push_check(row)
        self.repo_check(row)

    # def config_check(self, row_counter):
    #     msg = self.main.gitCommands.config_check(self.data.top_level_folders[row_counter - 1])

    def init_check(self, row_counter):
        self.log.debug("INIT check")
        result, msg = self.main.gitCommands.init_check(self.data.top_level_folders[row_counter])
        if result:
            self.gui.table_set_item_text(row_counter, 1, str(msg))
            self.gui.table_set_item_background(row_counter, 1, 'green')
        else:
            self.gui.table_set_item_text(row_counter, 1, str(msg))
            self.gui.table_set_item_background(row_counter, 1, 'red')

    def add_check(self, row_counter):
        self.log.debug("ADD check")
        result, msg = self.main.gitCommands.add_check(self.data.top_level_folders[row_counter])
        if result:
            self.gui.table_set_item_text(row_counter, 2, str(msg))
            self.gui.table_set_item_background(row_counter, 2, 'green')
        else:
            self.gui.table_set_item_text(row_counter, 2, str(msg))
            self.gui.table_set_item_background(row_counter, 2, 'red')

    def commit_check(self, row_counter):
        self.log.debug("COMMIT check")
        result, msg = self.main.gitCommands.commit_check(self.data.top_level_folders[row_counter])
        if result:
            self.gui.table_set_item_text(row_counter, 3, str(msg))
            self.gui.table_set_item_background(row_counter, 3, 'green')
        else:
            self.gui.table_set_item_text(row_counter, 3, str(msg))
            self.gui.table_set_item_background(row_counter, 3, 'red')

    def remote_check(self, row_counter):
        self.log.debug("REMOTE check")
        result, msg = self.main.gitCommands.remote_check(self.data.top_level_folders[row_counter])
        if result:
            self.gui.table_set_item_text(row_counter, 4, str(msg))
            self.gui.table_set_item_background(row_counter, 4, 'green')
        else:
            self.gui.table_set_item_text(row_counter, 4, str(msg))
            self.gui.table_set_item_background(row_counter, 4, 'red')

    def push_check(self, row):
        self.log.debug("REMOTE check")
        result, msg = self.main.gitCommands.push_check(self.data.top_level_folders[row])
        if result:
            self.gui.table_set_item_text(row, 5, str(msg))
            self.gui.table_set_item_background(row, 5, 'green')
        else:
            self.gui.table_set_item_text(row, 5, str(msg))
            self.gui.table_set_item_background(row, 5, 'red')

    def repo_check(self, row):
        result, msg = self.main.gitLabCommands.repo_check(self.data.top_level_folders[row])
        if result:
            self.gui.table_set_item_text(row, 6, str(msg))
            self.gui.table_set_item_background(row, 6, 'green')
        else:
            self.gui.table_set_item_text(row, 6, str(msg))
            self.gui.table_set_item_background(row, 6, 'red')

    def add_folder_to_remote(self, rows):
        for row_counter in rows:
            folder = self.data.top_level_folders[row_counter]
            filename = self.data.top_level_filenames[row_counter]
            self.log.debug("Add folder {} to remote".format(folder))
            self.log.debug("Folder:{}".format(folder))
            self.main.gitCommands.init(path=folder, row=row_counter)
            self.main.gitCommands.add(path=folder, row=row_counter)
            self.main.gitCommands.commit(path=folder, row=row_counter)
            self.main.gitCommands.remote(path=folder, row=row_counter)
            self.main.gitCommands.push(path=folder, row=row_counter)
            self.check_one_folder(row=row_counter, filename=filename)

    def pathname_to_filename(self, path):
        self.log.info("PATH to filename:{}".format(path))
        counter = 0
        for find_path in self.data.top_level_folders:
            if find_path == path:
                file_name = self.data.top_level_filenames[counter]
                return file_name
            counter = counter + 1
        return None

    def repo_name_to_list_number(self, name):
        counter = 0
        for find_name in self.data.top_level_filenames:
            if find_name == name:
                return counter
            else:
                counter = counter + 1
        return "error"

    @staticmethod
    def to_lowercase(name):
        lower_name = name.lower()
        return lower_name

    def show_error_message(self, msg):
        self.log.debug("Show error message: {}".format(msg))

    def delete_selected_local_git(self, rows):
        for row_counter in rows:
            self.log.debug('delete selected local git')
            repo_path = self.data.top_level_folders[row_counter]  # list is zero based
            self.main.gitCommands.delete_local_git(repo_path)
            self.perform_check(row_counter)

    def delete_selected_remote_git(self, rows):
        for row_counter in rows:
            self.log.debug('delete selected remote git')
            repo_path = self.data.top_level_folders[row_counter]  # list is zero based
            self.main.gitLabCommands.delete_remote_git(repo_path)
            self.repo_check(row_counter)
