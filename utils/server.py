import logging

from tornado.web import Application

import utils.constants as c


class Server(Application):
    """It instantiates and boostraps all application-related services.

    """

    def __init__(self):
        """Initialization method.

        Note that you will need to set your own arguments, handlers and
        default settings from Tornado.

        """

        # Defines own arguments to be avaliable for the class
        args = {
            'config': c.config
        }

        # Defines the handlers that will handle the requests
        handlers = [
        ]

        # Overriding the application class
        super(Server, self).__init__(handlers, debug=True, autoreload=True)
