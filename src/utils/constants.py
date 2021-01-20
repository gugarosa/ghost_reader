import os

from dotenv import load_dotenv

# Loads the environment variables
load_dotenv()

# Gathering and defining constants
# Server-related
SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_FILES_PATH = os.getenv('SERVER_FILES_PATH')
SERVER_SECRET_KEY = os.getenv('SERVER_SECRET_KEY')
SERVER_WORKERS = os.getenv('SERVER_WORKERS')

# Database-related
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_CONNECTION_TIME = os.getenv('DB_CONNECTION_TIME')

# GPU-related
GPU_MAX_LOAD = os.getenv('GPU_MAX_LOAD')
GPU_MAX_MEMORY = os.getenv('GPU_MAX_MEMORY')
