#!/usr/bin/env python

import os
import logging
from logging import handlers, Formatter

from Tools.UtilsManager import UtilsManager
from Tools.StatusCodes import StatusCodes
from Tools.EnvManager import EnvManager

def get_logger():
    logger = logging.getLogger("Terminator log")
    logger.setLevel(logging.DEBUG)
    
    log_file, byte_size, bck_count = get_log_file_attribs()
    ch = logging.handlers.RotatingFileHandler(log_file, maxBytes=byte_size, backupCount=bck_count)
    log_format = "[%(asctime)s: %(filename)s:%(lineno)s : %(funcName) 25s()] %(message)s"
    formatter = logging.Formatter(log_format)

    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


def get_log_file():
    pj_logs_dir = EnvManager().get_env_var("PJ_LOGS_DIR")
    cfg_reader = UtilsManager().get_config_parser()
    try:
        log_file = cfg_reader.get('main', 'LOG_FILE')
    except Exception as e:
        print "Error while getting log file", e.args
        return (StatusCodes.ERROR)
    return os.path.join(pj_logs_dir, log_file)


def get_log_file_attribs(get_byte_size=True, bck_count=True):
    cfg_reader = UtilsManager().get_config_parser()
    try:
        byte_size = cfg_reader.get('main', 'LOG_FILE_MAX_SIZE')
        byte_size = cfg_reader.get('main', 'LOG_FILE_NUM_BACKUPS')
    except Exception as e:
        print "Error while getting log file", e.args
        return (StatusCodes.ERROR)

    return (get_log_file(), byte_size, byte_size)

