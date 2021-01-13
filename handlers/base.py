import logging

from tornado.web import RequestHandler

import utils.database as d

logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):
    """Defines main possible requests and other necessary functions.

    """

    def set_config(self, **kwargs):
        """Sets a configuration object to the class itself.

        """

        # Defining the configuration object
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set_default_headers(self):
        """Sets the default response headers for an incoming request.

        """

        # Sets CORS-issue, authorized headers and allowed methods
        self.set_header('Access-Control-Allow-Origin',
                        '*')
        self.set_header('Access-Control-Allow-Headers',
                        'x-requested-with, Authorization, Content-type')
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, PATCH, DELETE, PUT')

    def initialize(self, **kwargs):
        """Basic initializer of every incoming request.

        """

        # Actually sets the configuration to the request
        self.set_config(**kwargs)

        # Connects the request to the database
        d.connect()
        
    def on_finish(self):
        """Basic finisher of every incoming request.

        """

        # Disconnects the request to the database
        d.disconnect()

    def handle_response(self, task, response_type):
        """Handles a response by outputting vital information.

        Args:
            task (str): Task identifier.
            response_type (str): Type of the response.

        Returns:
            A dictionary holding the response.

        """

        # Defines a response object to output
        res = {
            response_type: f'A {task} task is being added to the pool.'
        }

        # Logs the information
        logger.debug(res[response_type])

        return res

    def get_token(self):
        """Gets the authorization token from the request.

        Returns:
            The requested token.

        """

        try:
            # Gathering authorization token
            token = self.request.headers.get('Authorization').split(' ')[1]

        # If there is no token in the request
        except:
            # We apply an empty string as the token
            token = ''

        return token
