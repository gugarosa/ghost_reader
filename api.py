import logging
import signal
import sys

from tornado import autoreload
from tornado.ioloop import IOLoop

import utils.constants as c
from utils.server import Server

# Enables logging and gets its object
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _signal_handler(*args):
    """Forces the interruption signal to be intercepted by the main process.

    """

    logging.warning("Interrupting the server ...")

    # Exits the process
    sys.exit()


if __name__ == '__main__':
    # Logging important information
    logging.info('Starting server ...')

    # Setting the responsibility of who will receive the interruption signal
    signal.signal(signal.SIGINT, _signal_handler)

    # Logs its port
    logging.debug(f'Port: {c.SERVER_PORT}')

    # Creates an application
    app = Server()

    # Adds an autoreload hook in order to properly shutdown the workers pool
    autoreload.add_reload_hook(lambda: app.shutdown())

    # Servers the application on desired port
    app.listen(c.SERVER_PORT)

    # Starts a IOLoop instance
    IOLoop.current().start()
