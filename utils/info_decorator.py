import logging


def logging_config():
    level = logging.INFO
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)


def info_decorator(func, message=None):
    """
    :param func: the function to be executed
    :param message: optional message to print before executing the function
    :return: the same function decorated with the extra functionality
    """
    def wrapper(*args, **kwargs):
        logging_config()

        if message is None:
            m = f'::: RUNNING FUNCTION {str(func.__name__)} :::'
        else:
            m = message

        logging.info(m)
        func(*args, **kwargs)

    return wrapper
