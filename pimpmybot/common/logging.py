import logging


def get_logger(name, level=logging.WARNING):
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handler
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # Create formatter and set it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Set the handler to the logger
    logger.addHandler(handler)
    return logger
