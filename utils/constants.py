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
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_CONNECTION_TIME = os.getenv('DB_CONNECTION_TIME')

# GPU-related
GPU_MAX_LOAD = os.getenv('MAX_LOAD')
GPU_MAX_MEMORY = os.getenv('MAX_MEMORY')
