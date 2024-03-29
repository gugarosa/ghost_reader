import logging
from concurrent.futures import ProcessPoolExecutor

from tornado.web import Application

import utils.constants as c
from handlers import (ConvertHandler, ExtractHandler, LoginHandler,
                      RegisterHandler)
from utils.process_manager import ProcessManager

logger = logging.getLogger(__name__)


class Server(Application):
    """It instantiates and boostraps all application-related services.

    """

    def __init__(self):
        """Initialization method.

        Note that you will need to set your own arguments, handlers and
        default settings from Tornado.

        """

        # Defines the process manager
        self.process_manager = ProcessManager()

        # Creates a pool of workers
        self.pool = ProcessPoolExecutor(max_workers=int(c.SERVER_WORKERS))

        # Defines own arguments to be avaliable for the class
        args = {
            'process_manager': self.process_manager
        }

        # Defines the handlers that will handle the requests
        handlers = [
            (r'/api/convert', ConvertHandler, args),
            (r'/api/extract', ExtractHandler, args),
            (r'/api/login', LoginHandler, args),
            (r'/api/register', RegisterHandler, args),
        ]

        # Overriding the application class
        super(Server, self).__init__(handlers, debug=True, autoreload=True)

    def shutdown(self, blocking_call=True):
        """Closes the worker pools.

        Args:
            blocking_call (bool): Boolean to block itself until all pools are closed.

        """

        logger.warning('Shutting down workers pool ...')

        # Shutdowns the pool
        self.pool.shutdown(blocking_call)
