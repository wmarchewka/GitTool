from logger import Logger
from PySide2 import QtGui


class Data(object):
    def __init__(self):
        self.log = Logger().log
        self.top_level_push_path = '/Users/waltermarchewka/Desktop/GITLAB'
        self.top_level_pull_path = '/Users/waltermarchewka/Desktop/GITLAB_TEST'
        self.siemens_txt_url = 'git@code.siemens.com:siemensbte/drivers/'
        self.gitlab_txt_url = 'git@gitlab.com:siemensbte/drivers/'
        self.gitlab_api_url = 'https://gitlab.com/'
        self.gitlab_private_token = "zX3Sz3_-3XadLdHqD_tR"
        self.siemens_private_token = ""
        self.origin = 'origin'
        self.top_level_folders = []
        self.top_level_filenames = []
        self.url = None
        self.token = None
        self.color_purple = QtGui.QColor("purple")
        self.color_green = QtGui.QColor("green")
        self.color_red = QtGui.QColor("red")
        self.color_yellow = QtGui.QColor("yellow")
