from __future__ import absolute_import, unicode_literals

import logging
import os

from utils import DATA_DIRECTORY


LOG_PATH = os.path.join(DATA_DIRECTORY, 'log')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


def get_logger(name, level=logging.WARNING):
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)

    file_handler = logging.FileHandler(os.path.join(LOG_PATH, '{0}.log'.format(name)))
    file_handler.setLevel(level)

    # Create formatter and set it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Set the handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
