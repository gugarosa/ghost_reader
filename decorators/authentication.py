import base64
import json
import logging

import jwt

import utils.constants as c

logger = logging.getLogger(__name__)


def authenticate_user():
    """Checks whether the request is authenticated or not.

    Returns:
        It will call a wrapper function prior to the original one.

    """

    def check_auth(f):
        """Checks if user is authenticaed or not.

        Args:
            f (*): The original function to be wrapped.

        Returns:
            A wrapped function.

        """

        async def wrapper(*args, **kwargs):
            """Wraps the authentication verification.

            Returns:
                The demanded request if authentication is valid.

            """

            # Getting handler object
            handler = args[0]

            # Gets current token
            token = handler.get_token()

            # Trying to decode the token
            try:
                # If it is valid, this operation will not cause any error
                _ = jwt.decode(token, c.SERVER_SECRET, algorithms=['HS256'])

            # If it was not possible to decode
            except Exception:
                # Defines a response message
                msg = 'Token is not valid or has expired.'

                # Sets status and writes back an error message
                logger.debug(msg)
                handler.set_status(401)
                handler.write(dict(error=msg))

                return False

            return await f(*args, **kwargs)

        return wrapper

    return check_auth
