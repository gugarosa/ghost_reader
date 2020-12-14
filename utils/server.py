import logging
from concurrent.futures import ProcessPoolExecutor

from tornado.web import Application

import utils.constants as c
from handlers.extract import ExtractHandler
from utils.process_manager import ProcessManager


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
        self.pool = ProcessPoolExecutor(max_workers=int(c.WORKERS))

        # Defines own arguments to be avaliable for the class
        args = {
            'config': c.config,
            'process_manager': self.process_manager
        }

        # Defines the handlers that will handle the requests
        handlers = [
            (r'/api/extract', ExtractHandler, args),
        ]

        # Overriding the application class
        super(Server, self).__init__(handlers, debug=True, autoreload=True)

    def shutdown(self, blocking_call=True):
        """Closes the worker pools.

        Args:
            blocking_call (bool): Boolean to block itself until all pools are closed.

        """

        logging.warning('Shutting down workers pool ...')

        # Shutdowns the pool
        self.pool.shutdown(blocking_call)
