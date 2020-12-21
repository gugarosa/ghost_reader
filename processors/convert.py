import datetime
import logging
import os

import utils.constants as c
from models import Conversion, Extraction
from processors.base import BaseProcessor
from utils.speecher import Speecher

logger = logging.getLogger(__name__)


class ConvertProcessor(BaseProcessor):
    """A ConvertProcessor is in charge of consuming the conversion task.

    """

    def __init__(self):
        """Initialization method.

        """

        # Overriding the parent class
        super(ConvertProcessor, self).__init__()

    def _register_task(self, task):
        """Registers a task into the database.

        Args:
            task (dict): The task to be consumed.

        Returns:
            The task's identifier.

        """

        # Gathers the correlated extraction object
        e = Extraction.objects.get(id=task['extraction_id'])

        # Creates a conversion object
        cs = Conversion(extraction=e, status='started', created_at=datetime.datetime.utcnow,
                        updated_at=datetime.datetime.utcnow)

        # Saves to the database
        cs.save()

        return cs.id

    def _invoke_consume(self, _id, task):
        """Runs the actual learning job.

        This method runs on multiple parallel executors, which can be either threads or processes.
        Anything that this method returns should be pickable (including possible
        cython sub-objects).

        Args:
            _id (str): Hex string holding the task's id.
            task (dict): The task to be consumed.

        """

        logger.debug('Consuming task ...')

        # Gathers the object
        cs = Conversion.objects.get(id=_id)

        # Gathers the local file path
        local_path = cs.extraction.local_path + '_' + task['language'] + '.ogg'

        # Initializes the text-to-speecher
        s = Speecher(language=task['language'])

        # Saves the desired text to a file
        s.save(cs.extraction.text, local_path)

        # Runs the speecher
        s.run()

        # Update its attributes
        cs.local_path = local_path
        cs.status = 'success'
        cs.updated_at = datetime.datetime.utcnow

        # Saves to the db
        cs.save()

        logger.debug('Task consumed.')
