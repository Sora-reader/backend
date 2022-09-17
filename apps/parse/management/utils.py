import logging


def mute_logger_stdout(logger_name: str, *other_loggers):
    import warnings

    logger_names = [logger_name, *other_loggers]
    for name in logger_names:
        warnings.filterwarnings("ignore", module=name)
        logger = logging.getLogger(name)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False
