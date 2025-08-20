
import logging, sys
from pythonjsonlogger import jsonlogger
def setup_logger(name='bot'):
    logger = logging.getLogger(name)
    if logger.handlers: return logger
    logger.setLevel(logging.INFO)
    h = logging.StreamHandler(sys.stdout)
    fmt = '%(asctime)s %(levelname)s %(name)s %(message)s'
    h.setFormatter(jsonlogger.JsonFormatter(fmt))
    logger.addHandler(h)
    return logger
