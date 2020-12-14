from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    """Defines main possible requests and other necessary functions.

    """

    def initialize(self, **kwargs):
        """It serves as the basic initializer of every incoming request.

        """

        # Defining the configuration object
        self.config = kwargs.get('config')

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

        return res
