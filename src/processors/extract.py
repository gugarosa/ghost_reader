import datetime
import logging
import os

from pdfminer.high_level import extract_text

import utils.constants as c
import utils.loader as l
from models import Extraction
from processors import BaseProcessor

logger = logging.getLogger(__name__)


class ExtractProcessor(BaseProcessor):
    """An ExtractProcessor is in charge of consuming the learning task.

    """

    def __init__(self):
        """Initialization method.

        """

        # Overriding the parent class
        super(ExtractProcessor, self).__init__()

    def _register_task(self, task):
        """Registers a task into the database.

        Args:
            task (dict): The task to be consumed.

        Returns:
            The task's identifier.

        """

        # Creates an extraction object
        e = Extraction(url=task['pdf_url'], status='started', created_at=datetime.datetime.utcnow,
                       updated_at=datetime.datetime.utcnow)

        # Saves to the database
        e.save()

        return e.id

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

        # Gets the information needed
        pdf_url = task['pdf_url']
        pdf_path = c.SERVER_FILES_PATH + os.path.basename(pdf_url)

        # Downloads a file
        l.download_file(pdf_url, pdf_path)

        # Extracting text from file
        text = extract_text(pdf_path)

        # Gathers the object, update its attributes and
        e = Extraction.objects.get(id=_id)

        # Update its attributes
        e.text = text
        e.local_path = pdf_path
        e.status = 'success'
        e.updated_at = datetime.datetime.utcnow

        # Saves to the db
        e.save()

        logger.debug('Task consumed.')
