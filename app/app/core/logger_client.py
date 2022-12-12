import logging
import datetime

from app.core.config import settings

class LoggerClient():    
    def getLogger(self, name):
        """
        > The function configures the logging module to use UTC time, and then returns a logger object
        
        :param name: The name of the logger
        :return: A logger object.
        """
        logging.basicConfig(level=logging.getLevelName(settings.LOG_LEVEL.upper()), format='datetime="%(asctime)s" level=%(levelname)s %(message)s module=%(name)s')
        logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))
        return logging.getLogger(name)

logger_client = LoggerClient()
