import configparser

# Initializes the configuration object and read it
config = configparser.ConfigParser()
config.read('config.ini')

# Gathering and defining constants
# Server-related
PORT = config.get('SERVER', 'PORT')
PATH = config.get('SERVER', 'PATH')

# GPU-related
GPU_MAX_LOAD = config.get('GPU', 'MAX_LOAD')
GPU_MAX_MEMORY = config.get('GPU', 'MAX_MEMORY')

# Workers-related
WORKERS = config.get('WORKERS', '')