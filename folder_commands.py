from logger import Logger
import os
import subprocess

PIPE = subprocess.PIPE


class FolderCommands(object):

    def __init__(self, gui):
        self.log = Logger().log
        self.horizontal_column_selected = None
        self.vertical_row_selected = None
        self.selected_item = None
        self.gui = gui

    def get_folder_list(self, top_level_path):
        top_level_folders = []
        top_level_filenames = []
        if top_level_path is not None:
            row_counter = 0
            filenames = os.listdir(top_level_path)
            for filename in filenames:  # loop through all the files and folders
                filename_lowercase = self.to_lowercase(filename)
                full_path = os.path.join(top_level_path, filename_lowercase)
                if os.path.isdir(full_path):
                    top_level_folders.append(full_path)
                    top_level_filenames.append(filename_lowercase)
            top_level_folders.sort()
            top_level_filenames.sort()
            for filename in top_level_filenames:
                row_counter = row_counter + 1
                self.gui.table_set_item_text(row=row_counter, column=0, text=filename)
                if self.check_for_git_folder(top_level_folders[row_counter - 1]):
                    self.gui.table_set_item_color(row_counter, 0, 'green')
                else:
                    self.gui.table_set_item_color(row_counter, 0, 'red')
        else:
            self.show_error_message("Please select local Path")

    def check_for_git_folder(self, path):
        # self.log.info("Check for GIT folder:{}".format(path))
        process = subprocess.Popen(["git", "status", "-u", "no"], cwd=path, stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()
        # self.log.info("STATUS:{}  ERROR:{}".format(stdoutput, stderroutput))
        if stderroutput:
            msg = "ERROR this is NOT a .git repository"
            # self.log.info(msg)
            return False
        else:
            msg = "SUCCESS this is a .git repository"
            # self.log.info(msg)
            return True

    def add_folders_to_remote(self):
        self.gui.tb_Repos.clearContents()
        self.gui.table_setup()
        all_record = ""
        row_counter = 0
        self.log.info("Folders:{}".format(self.top_level_folders))
        for folder in self.top_level_folders:
            row_counter = row_counter + 1
            self.log.info("Folder:{}".format(folder))
            self.git_commands.init(folder=folder, row_counter=row_counter)
            self.git_commands.add(folder=folder, row_counter=row_counter)
            self.git_commands.commit(folder=folder, row_counter=row_counter)
            self.git_commands.show(folder=folder, row_counter=row_counter)
            self.git_commands_push(folder=folder, row_counter=row_counter, lowercase_folder=folder)

    def add_all_to_remote_clicked(self):
        self.add_folders_to_remote()

    @staticmethod
    def to_lowercase(name):
        lower_name = name.lower()
        return lower_name

    def show_error_message(self, msg):
        self.log.info("Show error message: {}".format(msg))
