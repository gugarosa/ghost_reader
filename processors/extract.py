import datetime
import logging
import os

from pdfminer.high_level import extract_text

import utils.constants as c
import utils.loader as l
from processors.base import BaseProcessor

logger = logging.getLogger(__name__)


class ExtractProcessor(BaseProcessor):
    """A TrainerProcessor class is in charge of consuming the learning task.

    """

    def __init__(self):
        """Initialization method.
        """

        # Overriding the parent class
        super(ExtractProcessor, self).__init__()

    def _invoke_consume(self, task):
        """Runs the actual learning job.

        This method runs on multiple parallel executors, which can be either threads or processes.
        Anything that this method returns should be pickable (including possible
        cython sub-objects).

        Args:
            task (dict): The task to be consumed.

        """

        logger.debug('Consuming task ...')
        
        # Gets the information needed
        pdf_url = task['pdf_url']
        pdf_path = c.SERVER_PATH + os.path.basename(pdf_url)

        # Downloads a file
        l.download_file(pdf_url, pdf_path)

        # Extracting text from file
        text = extract_text(pdf_path)

        # Adds imoprtant information to the callback
        task['callback']['status'] = 'success'
        task['callback']['pdf_path'] = pdf_path
        task['callback']['text'] = text

        logger.debug(f'Task callback: {task["callback"]}')
