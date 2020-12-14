import datetime
import logging

import tornado

import utils.messaging as m
from handlers.base import BaseHandler


class TrainerHandler(BaseHandler):
    """Defines all possible methods for extract information (text) from a PDF.

    """

    def initialize(self, **kwargs):
        """Initializes the current handler.

        """

        # Gathers the config, process manager and processor objects
        self.config = kwargs.get('config')
        self.process_manager = kwargs.get('process_manager')
        self.processor = TrainerProcessor

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        # Creating the data object
        data = {
            'callback': {
                'start_time': datetime.datetime.utcnow().isoformat()
            }
        }

        # Tries to add a new process to the pool
        try:
            logging.info('Adding extract task to the pool ...')

            # Adding process to the pool
            self.process_manager.add_process({
                'target': self.processor,
                'data': data
            })

        # If process could not be added to the pool, reply with an error
        except Exception as e:
            logging.exception(e)

            # Sets status  to error and writes back
            self.set_status(500)
            self.finish(m.handler_error('extract'))

            return False

        # Writes back a success message
        self.finish(m.handler_success('extract'))

        return True
