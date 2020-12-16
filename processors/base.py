import datetime
import logging
import os

from mongoengine import connect

import utils.constants as c

logger = logging.getLogger(__name__)



class BaseProcessor:
    """Consumes any type of tasks.

    """

    def consume(self, task):
        """This method should be invoked by the workers on a pool to run the task.

        Notice that this method just shelters the actual code that will be executed,
        so any internal asynchronous exception will stay trapped here and logged explicitly.

        Args:
            task (dict): The task to be consumed.

        """

        # Tries to consume the task
        try:
            logger.debug('Sending task to worker ...')
            
            # Connects to the database
            connect(host=c.DB_HOST)

            # Register the task and gathers its identifier
            _id = self._register_task(task)

            # Consumes the task
            self._invoke_consume(_id, task)

            logger.debug('Worker has finished the task.')

        # If an exception has happened, logs it
        except Exception as e:
            logger.exception(e)

    def _register_task(self, task):
        """Registers a task into the database.

        Args:
            task (dict): The task to be consumed.
        
        """

        raise NotImplementedError

    def _invoke_consume(self, task):
        """Runs the actual task.

        This method runs on multiple parallel executors, which can be either threads or processes.
        Anything that this method returns should be pickable (including possible
        cython sub-objects).

        Args:
            task (dict): The task to be consumed.

        """

        raise NotImplementedError
