import base64
import json

import jwt

import utils.constants as c


def auth():
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
                # Sets an unauthorized status
                handler.set_status(401)

                # Writes back an error message
                handler.write(dict(error='Token is not valid or has expired.'))

                return False

            return f(*args, **kwargs)

        return wrapper

    return check_auth
