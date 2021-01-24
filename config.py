import configparser
import os
from logger import Logger


class Config(object):
    def __init__(self):
        self.log = Logger().log
        self.config = configparser.ConfigParser()
        self.cwd = os.getcwd() + '/config/'
        self.ini_filename = "config.ini"
        self.ini_path = os.path.join(self.cwd, self.ini_filename)
        self.open()
        self.get_version()

    def open(self):
        try:
            self.config.read(self.ini_path)
        except Exception as e:
            self.log.debug("No INI file")
        else:
            return True

    def read_key(self, section, key):
        try:
            value = self.config.get(section, key)
            self.log.debug("value:{}".format(value))
            return value
        except configparser.NoSectionError:
            self.log.debug("No section")
            self.create_default_sections()  # assumefile not created
            value = self.config.get(section, key)
            self.log.debug("READ VALUE:{}".format(value))
            return value

    def write_key(self, section, key, value):
        self.config.set(section, key, value)
        self.save_file()

    def save_file(self):
        with open(self.ini_path, 'w') as configfile:  # save
            self.config.write(configfile)

    def get_version(self):
        version = self.read_key('VERSION', 'version')

    def create_default_sections(self):
        self.config.add_section("VERSION")
        self.config.add_section('PATHS')
        self.config.set('VERSION', 'version', '1.0')
        self.config.set('PATHS', 'local_push_path', '')
        self.config.set('PATHS', 'local_pull_path', '')
        self.save_file()
