import logging
import logging.config
import os


class Logger(object):
    """    THIS MODULE IS A SINGLETON !! WE DONT NEED MORE THAN ONE INSTANCE OF THE CLASS SO WE LIMIT TO ONE
    INSTANCE OF THE CLASS.  The module used for logging to console, and file.  uses a logging.ini file to setup all
    logging parameters.
    """
    _instance = None
    _init = None
    __version__ = '0.0.2'

    def __new__(cls, disabled=False, level=None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            logging.basicConfig(level='CRITICAL')
            logging.info("{} INSTANTIATING...".format(__name__))

        return cls._instance

    # ****************************************************************************************************
    def __init__(self, disabled=False, level=logging.DEBUG):
        if Logger._init is None:
            Logger._init = "init"
            if os.name is "nt":
                self.log_config_file_path = r"config/logging.ini"
            else:
                self.log_config_file_path = "config/logging.ini"
            self.log = logging.getLogger('logger')
            self.create_log_folder(disabled, level)
            self.log.info('{} INITIALIZING....'.format(__name__))
            self.log.info("LOG LEVEL {}".format(self.log.getEffectiveLevel()))
            self.log.info("{} init complete...".format(__name__))

    # ****************************************************************************************************
    def set_log_level(self, log_level):
        self.log.info("Setting LOG LEVEL to:{}".format(log_level))
        self.log.setLevel(log_level)

    # ****************************************************************************************************
    @staticmethod
    def shutdown():
        logging.shutdown()

    # ****************************************************************************************************
    def create_log_folder(self, disabled, level):
        cwd = os.getcwd()
        self.log.info("Check for LOG folder at :{}".format(self.log_config_file_path))
        self.log.info("CWD is:{}".format(cwd))
        if not os.path.exists(cwd + '/logs'):
            os.makedirs('logs')
        logging.config.fileConfig(self.log_config_file_path)
        self.log.disabled = disabled
        self.log.setLevel(level)
