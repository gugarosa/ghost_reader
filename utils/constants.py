import os

from dotenv import load_dotenv

# Loads the environment variables
load_dotenv()

# Gathering and defining constants
# Server-related
SERVER_PORT = os.getenv('PORT')
SERVER_FILES_PATH = os.getenv('FILES_PATH')
SERVER_SECRET_KEY = os.getenv('SECRET_KEY')
SERVER_WORKERS = os.getenv('WORKERS')

# Database-related
DB_ALIAS = os.getenv('ALIAS')
DB_CONNECTION_TIME = os.getenv('CONNECTION_TIME')
DB_HOST = os.getenv('HOST')

# GPU-related
GPU_MAX_LOAD = os.getenv('MAX_LOAD')
GPU_MAX_MEMORY = os.getenv('MAX_MEMORY')
