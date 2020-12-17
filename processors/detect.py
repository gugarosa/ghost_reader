import os
import logging
import datetime

from models.detection import Detection
from models.extraction import Extraction
from processors.base import BaseProcessor
from utils.speecher import Speecher

import utils.constants as c

logger = logging.getLogger(__name__)


class DetectProcessor(BaseProcessor):
    """A DetectProcessor is in charge of consuming the detection task.

    """

    def __init__(self):
        """Initialization method.

        """

        # Overriding the parent class
        super(DetectProcessor, self).__init__()

    def _register_task(self, task):
        """Registers a task into the database.

        Args:
            task (dict): The task to be consumed.

        Returns:
            The task's identifier.

        """

        # Gathers the correlated extraction object
        e = Extraction.objects.get(id=task['_id'])

        # Creates a detection object
        d = Detection(extraction=e, status='started', created_at=datetime.datetime.utcnow,
                      updated_at=datetime.datetime.utcnow)

        # Saves to the database
        d.save()

        return d.id

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
        d = Detection.objects.get(id=_id)

        # Gathers the local file path
        local_path = d.extraction.local_path + '.ogg'

        # Initializes the text-to-speecher
        s = Speecher(language=c.SPEECH_LANGUAGE)

        # Saves the desired text to a file
        s.save(d.extraction.text, local_path)

        # Runs the speecher
        s.run()

        # Update its attributes
        d.local_path = local_path
        d.status = 'success'
        d.updated_at = datetime.datetime.utcnow

        # Saves to the db
        d.save()

        logger.debug('Task consumed.')
