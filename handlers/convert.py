import datetime
import logging

import tornado

from handlers import BaseHandler
from processors import ConvertProcessor

# Creates a constant that defines the type of task
TASK_IDENTIFIER = 'convert'

logger = logging.getLogger(__name__)


class ConvertHandler(BaseHandler):
    """Defines all possible methods for converting information (text) to voice (audio).

    """

    def initialize(self, **kwargs):
        """Basic initializer of every incoming request.

        """

        # Defines extra key-word arguments
        kwargs['processor'] = ConvertProcessor

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
        extraction_id = req['extraction_id']
        language = req['language']

        # Creating the data object
        data = {
            'extraction_id': extraction_id,
            'language': language
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

            # Sets status  to error and writes back
            self.set_status(500)
            self.finish(self.handle_response(TASK_IDENTIFIER, 'error'))

            return False

        # Writes back a success message
        self.finish(self.handle_response(TASK_IDENTIFIER, 'success'))

        return True
