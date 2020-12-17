import configparser

# Initializes the configuration object and read it
config = configparser.ConfigParser()
config.read('config.ini')

# Gathering and defining constants
# Server-related
SERVER_PORT = config.get('SERVER', 'PORT')
SERVER_PATH = config.get('SERVER', 'PATH')
SERVER_WORKERS = config.get('SERVER', 'WORKERS')

# Database-related
DB_ALIAS = config.get('DB', 'ALIAS')
DB_CONNECTION_TIME = config.get('DB', 'CONNECTION_TIME')
DB_HOST = config.get('DB', 'HOST')

# GPU-related
GPU_MAX_LOAD = config.get('GPU', 'MAX_LOAD')
GPU_MAX_MEMORY = config.get('GPU', 'MAX_MEMORY')

# Speech-related
SPEECH_LANGUAGE = config.get('SPEECH', 'LANGUAGE')
