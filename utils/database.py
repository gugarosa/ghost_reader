import logging
import utils.constants as c

from mongoengine import connect as _connect
from mongoengine import disconnect as _disconnect
from pymongo.errors import ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

def connect():
    """Performs a connection to the database.

    Note that this function wraps mongoengine's connection to provide additional logging.

    """

    # Attempts to connect to the database
    try:
        #
        _connect(serverSelectionTimeoutMS=c.DB_CONNECTION_TIME)

    # If an error occurs
    except ServerSelectionTimeoutError as e:
        logger.error(e)


def disconnect():
    """Performs a disconnection to the database.

    """

    # Disconnects the database
    _disconnect()