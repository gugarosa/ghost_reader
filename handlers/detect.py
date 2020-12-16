import datetime
import logging

import tornado
from mongoengine import connect

import utils.constants as c
from handlers.base import BaseHandler
from processors.detect import DetectProcessor

# Creates a constant that defines the type of task
TASK_IDENTIFIER = 'detect'

logger = logging.getLogger(__name__)

class DetectHandler(BaseHandler):
    """Defines all possible methods for detect information (text) to voice (audio).

    """

    def initialize(self, **kwargs):
        """Basic initializer of every incoming request.

        """

        # Defines extra key-word arguments
        kwargs['processor'] = DetectProcessor

        # Actually sets the configuration to the request
        self.set_config(**kwargs)
