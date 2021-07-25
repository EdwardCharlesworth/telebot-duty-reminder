import logging


def endless_try(func):
    def inner(*args, **kwargs):
        while(True):
            try:
                func(*args, **kwargs)
                logging.info(f'{func.__name__} end')

            except Exception as e:
                logging.error(e)
                logging.info(f'{func.__name__} restart')

    return inner


def log_function(func):
    def inner(*args, **kwargs):
        logging.info(f'{func.__name__} start')
        func(*args, **kwargs)
        logging.info(f'{func.__name__} end')

    return inner
