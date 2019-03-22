import logging


class V2RayLogger(object):
    _logger = None

    @classmethod
    def init_logger(cls, debug: bool = False):
        if cls._logger is None:
            cls._logger = logging.getLogger('V2Ray.Stats')
            console_handler = logging.StreamHandler()

            formatter = logging.Formatter('[%(levelname)s][%(asctime)s] [%(name)s][%(module)s]: %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            console_handler.setFormatter(formatter)
            if debug:
                cls._logger.setLevel(logging.DEBUG)
                console_handler.setLevel(logging.DEBUG)
            else:
                cls._logger.setLevel(logging.INFO)
                console_handler.setLevel(logging.INFO)

            cls._logger.addHandler(console_handler)
            if debug:
                cls._logger.debug('Debug mode on.')
        return cls

    @classmethod
    def info(cls, *args, **kwargs):
        if cls._logger is None:
            cls.init_logger()
        return cls._logger.info(*args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        if cls._logger is None:
            cls.init_logger()
        return cls._logger.error(*args, **kwargs)

    @classmethod
    def debug(cls, *args, **kwargs):
        if cls._logger is None:
            cls.init_logger()
        return cls._logger.debug(*args, **kwargs)
