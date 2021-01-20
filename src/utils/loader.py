import logging
import os
import urllib.request

logger = logging.getLogger(__name__)


def download_file(url, output_path):
    """Downloads a file given its URL and the output path to be saved.

    Args:
        url (str): URL to download the file.
        output_path (str): Path to save the downloaded file.

    """

    logger.debug(f'Downloading file from: {url}')

    # Checks if file exists
    file_exists = os.path.exists(output_path)

    # If file does not exist
    if not file_exists:
        # Downloads the file
        urllib.request.urlretrieve(url, output_path)

        logger.debug(f'File saved to: {output_path}.')

    # If file exists, just send a warning
    else:
        logger.warning('File already exists.')
