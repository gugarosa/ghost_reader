from models.detection import Detection
from processors.base import BaseProcessor

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

        pass

    def _invoke_consume(self, _id, task):
        """Runs the actual learning job.

        This method runs on multiple parallel executors, which can be either threads or processes.
        Anything that this method returns should be pickable (including possible
        cython sub-objects).

        Args:
            _id (str): Hex string holding the task's id.
            task (dict): The task to be consumed.

        """

        pass