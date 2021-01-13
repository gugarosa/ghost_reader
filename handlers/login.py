import datetime
import hashlib
import hmac
import logging

import jwt
import tornado
from mongoengine import connect

import utils.constants as c
from handlers import BaseHandler
from models import User

logger = logging.getLogger(__name__)


class LoginHandler(BaseHandler):
    """Defines all the activity prior to the user entering the system.

    """

    def initialize(self, **kwargs):
        """Basic initializer of every incoming request.

        """

        # Actually sets the configuration to the request
        self.set_config(**kwargs)

        # Connects the process to the database
        # connect()

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
            u = User.objects.get(username=username, password=password)

            # Defining the payload to further encode into a token
            payload = {
                'username': u.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
            }

            # Encoding payload in a token
            token = jwt.encode(payload, c.SERVER_SECRET_KEY, algorithm='HS256')

            # Logs and writes back the token
            logger.debug(token)
            self.write(dict(success=token.decode()))

            return True

        except:
            # Defines a response message
            msg = 'Invalid credentials.'

            # Sets status to error, logs and writes back
            logger.debug(msg)
            self.set_status(401)
            self.finish(dict(error=msg))

            return False
