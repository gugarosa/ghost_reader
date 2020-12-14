import logging
import queue as queue_lib
import signal
import sys
from multiprocessing import Process, Queue

import GPUtil
from tornado.ioloop import IOLoop

import utils.constants as c


class ProcessManager:
    """Controls the multi-processing features of this application.

    """

    def __init__(self):
        """Initialization method.

        """

        # Creates a queue object
        self.queue = Queue()

        # Creates an process object with a specific target
        self.current_process = Process(target=self._handle_process, args=(self.queue,),
                                       daemon=False)

        # Starts the process
        self.current_process.start()

    def _handle_process(self, queue):
        """It handles a new process by calling a specific IOLoop and starting it with a callback.

        Args:
            queue (Queue): A queue object.

        """

        # Creates an IOLoop object, spawns the callback and starts the loop
        loop = IOLoop()
        loop.spawn_callback(self._worker, queue)
        loop.start()

    def add_process(self, process):
        """Adds a new process to the queue.

        Args:
            process (Process): A new process to be added to the queue.

        """

        # Puts a new process in the queue
        self.queue.put(process)

    def _get_gpu_config(self):
        """Gathers the amount of load and memory that a process should use on the GPU.

        Returns:
            The amount of load and memory that a process should use.

        """

        # Gathers the load  and memory per process
        load_per_process = float(c.GPU_MAX_LOAD)
        mem_per_process = float(c.GPU_MAX_MEMORY)

        return load_per_process, mem_per_process

    def _get_device(self):
        """Gathers an avaliable GPU or CPU for further processing.

        Returns:
            A configuration object containing the device's information.

        """

        # Tries to check if there is an avaliable GPU
        try:
            # Gathers a list of GPUs
            gpus = GPUtil.getGPUs()

            # For each GPU
            for g in gpus:
                # Logs its information
                logging.info(g.name)

            # Calculates the load and memory per process
            load_per_process, mem_per_process = self._get_gpu_config()

            # Calculates the maximum possible load and memory for an avaliable GPU
            max_load = 1 - load_per_process
            max_mem = 1 - mem_per_process

            # Gathers the first avaliable GPU
            device_id = GPUtil.getFirstAvailable(order='first', maxLoad=max_load,
                                                 maxMemory=max_mem, attempts=3,
                                                 interval=3, verbose=False)[0]

            # Checks if the device id exists
            if device_id is not None:
                # Creates an object
                config = {
                    'gpu': {
                        'DEVICE_ID': device_id,
                        'MEMORY_FRACTION': mem_per_process
                    }
                }

                return config

        # If there is no avaliable GPU
        except Exception as e:
            logging.warning(e)

            # Creates a different object
            config = {
                'cpu': {
                }
            }

            return config

    def _drain_pool(self, pool):
        """Drains all lingering processes in the pool.

        Args:
            pool (list): The pool itself.

        Returns:
            The drained pool.

        """

        # Creates a new pool
        new_pool = []

        # For every process in the pool
        for p in pool:
            # Checks if the process is alive
            if not p.is_alive():
                # If not, terminates it
                p.terminate()

            # If it is alive
            else:
                # Appends the process to the new pool
                new_pool.append(p)

        return new_pool

    async def _worker(self, queue):
        """The worker method itself.

        Essentially, it is responsible for draining and adding new processes to the pool.

        Args:
            queue (Queue): A queue object.

        """

        def __empty_process_pool(pool):
            """Empties a pool of processes.

            Args:
                pool (list): The pool to be emptied.

            """

            # For every process in the pool
            for p in pool:
                # Terminates the process
                p.terminate()

        def __signal_handler(*args):
            """Forces the interruption signal to be intercepted by the main process.

            """

            # Empties the CPU and GPU pools
            __empty_process_pool(cpu_pool)
            __empty_process_pool(gpu_pool)

            logging.warning('Interrupting the process manager ...')

            # Exits the process
            sys.exit()

        # Initialize the job flag as false
        job = False

        # Creates empty lists for the CPU and GPU pools
        cpu_pool, gpu_pool = [], []

        # Setting the responsibility of who will receive the interruption signal
        signal.signal(signal.SIGINT, __signal_handler)

        # While the loop is true
        while True:
            # Tries to the drain the pools and add a process
            try:
                # Drains the CPU and GPU pool
                cpu_pool = self._drain_pool(cpu_pool)
                gpu_pool = self._drain_pool(gpu_pool)

                # Gathers the current job
                job = queue.get()

                # If the job exists
                if job:
                    # Gathers the processor
                    processor = job['target']()

                    # Gathers the device configuration
                    device = self._get_device()

                    # Adds to the job object the device configuration
                    job['data']['device_config'] = device

                    # If the device configuration is set to the GPU
                    if device.get('gpu'):
                        # Creates the process
                        p = Process(target=processor.consume,
                                    name='ghost_gpu-' + str(len(gpu_pool) + 1),
                                    args=(job['data'],), daemon=False)

                        # Starts the process
                        p.start()

                        # Appends the process to the GPU pool
                        gpu_pool.append(p)

                        logging.info('Adding process to GPU pool ...')

                    # If the device configuration is set to the CPU
                    else:
                        # Creates the process
                        p = Process(target=processor.consume,
                                    name='ghost_cpu-' + str(len(cpu_pool) + 1),
                                    args=(job['data'],), daemon=False)

                        # Starts the process
                        p.start()

                        # Appends the process to the CPU pool
                        cpu_pool.append(p)

                        logging.info('Adding process to CPU pool ...')

            # Whenever the queue is empty, logs the exception
            except queue_lib.Empty as e:
                logging.warning(e)
