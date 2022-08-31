# MAIN CONFIG FILE STRUCTURE
MAIN_CONFIG_FILES = "config_files"

LOGGER_CONFIG = "logger"
LOGGER_CONFIG_NAME = "name"
LOGGER_CONFIG_LEVEL = "level"
LOGGER_CONFIG_LEVEL_DICT = {"CRITICAL" : "CRITICAL",
                            "FATAL" : "FATAL",
                            "ERROR" : "ERROR",
                            "WARNING" : "WARNING",
                            "WARN" : "WARN",
                            "INFO" : "INFO",
                            "DEBUG" : "DEBUG",
                            "NOTSET" : "NOTSET"}
LOGGER_CONFIG_FORMAT = """from ConsulManager.Logger import logger, CONSUL_MANAGER_LOG_NAME
import logging

GRPC_MANAGER_NAME = "{name}"

log = logging.getLogger(f'{{CONSUL_MANAGER_LOG_NAME}}.{{GRPC_MANAGER_NAME}}')
log.setLevel(logging.{level})

"""

# CONFIG FILE STRUCTURE
CONFIG_DEFINITIONS = "definitions"



# INIT FILES
INIT_FILE_NAME = "__init__.py"
INIT_FILE_FORMAT = """# {name}
{logger}

{definitions}
"""
