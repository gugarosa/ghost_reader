import datetime
import hashlib
import hmac
import logging

import tornado

import utils.constants as c
from handlers import BaseHandler
from models import User

logger = logging.getLogger(__name__)


class RegisterHandler(BaseHandler):
    """Handles every new register request incoming to the API.

    """

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        # Gets the request
        req = tornado.escape.json_decode(self.request.body)

        # Gathering the request meta-information
        username = req['username']
        password = hmac.new(c.SERVER_SECRET_KEY.encode(), req['password'].encode(), hashlib.sha256).hexdigest()

        try:
            # Gathers the correlated user object
            u = User.objects.get(username=username)

            # Defines a response message
            msg = 'User already exists.'

            # Sets status to error, logs and writes back
            logger.debug(msg)
            self.set_status(500)
            self.finish(dict(error=msg))

            return False

        except:
            # Creates an user object
            u = User(username=username, password=password, created_at=datetime.datetime.utcnow,
                     updated_at=datetime.datetime.utcnow)

            # Saves to the database
            u.save()

            # Defines a response message
            msg = 'New user registered.'

            # Logs and writes back the response
            logger.debug(msg)
            self.write(dict(success=msg))

        return True
