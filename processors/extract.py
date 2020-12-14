import datetime
import logging
import os

from processors.base import BaseProcessor


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

        logging.debug(f'Task callback: {task["callback"]}')
