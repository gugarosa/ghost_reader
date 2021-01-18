# Using an official Python runtime as a parent image
FROM python:3.7-slim

# Gathers list of packages
RUN apt-get update

# Installs G++ for compiling fasttext
RUN apt-get install -y g++

# Creates the application's directory
RUN mkdir -p /ghost_reader

# Sets the work directory to application's folder
WORKDIR /ghost_reader

# Copy files into application's folder
COPY . .

# Copy the host's configuration example as the container's configuration file
COPY .env.example .env

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Execute the application when the container launches
CMD ["python", "api.py"]