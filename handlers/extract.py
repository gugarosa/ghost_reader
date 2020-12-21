import datetime
import logging

import tornado

from handlers import BaseHandler
from processors import ExtractProcessor

# Creates a constant that defines the type of task
TASK_IDENTIFIER = 'extract'

logger = logging.getLogger(__name__)


class ExtractHandler(BaseHandler):
    """Defines all possible methods for extract information (text) from a PDF.

    """

    def initialize(self, **kwargs):
        """Basic initializer of every incoming request.

        """

        # Defines extra key-word arguments
        kwargs['processor'] = ExtractProcessor

        # Actually sets the configuration to the request
        self.set_config(**kwargs)

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        # Gets the request
        req = tornado.escape.json_decode(self.request.body)

        # Gathering the request meta-information
        pdf_url = req['pdf_url']

        # Creating the data object
        data = {
            'pdf_url': pdf_url
        }

        # Tries to add a new process to the pool
        try:
            # Adding process to the pool
            self.process_manager.add_process({
                'target': self.processor,
                'data': data
            })

        # If process could not be added to the pool, reply with an error
        except Exception as e:
            logger.exception(e)

            # Sets status to error and writes back
            self.set_status(500)
            self.finish(self.handle_response(TASK_IDENTIFIER, 'error'))

            return False

        # Writes back a success message
        self.finish(self.handle_response(TASK_IDENTIFIER, 'success'))

        return True
