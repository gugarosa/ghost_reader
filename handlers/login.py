import hashlib
from datetime import datetime, timedelta

import jwt
import tornado

from handlers.base import BaseHandler
from models.user import User


class LoginHandler(BaseHandler):
    """Defines all the activity prior to the user entering the system.

    """

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        try:
            # Getting authentication object
            res = tornado.escape.json_decode(self.request.body)

            # Recovering username
            username = res['username']

            # Encoding password
            password = hashlib.sha256(res['password'].encode()).hexdigest()

        # If authentication object was not found, reply with an error
        except:
            # Setting status to bad request
            self.set_status(400)

            # Writing back an error message
            self.write(dict(error='Missing either username or password.'))

            return False

        # Performing query in database to check if user exists
        query = self.db(User).find_one(
            {'username': username, 'password': str(password)})

        # If user does not exists
        if not query:
            # Reply with an unauthorized error
            self.set_status(401)

            # Writing an error message
            self.write(dict(error='Invalid credentials.'))

            return False

        # Defining the payload to further encode into a token
        payload = {
            'username': query.username,
            'exp': datetime.utcnow() + timedelta(seconds=3600)
        }

        # Encoding payload in a token
        token = jwt.encode(payload, self.config.get(
            'API', 'SECRET'), algorithm='HS256')

        # Writing token back
        self.write(dict(success=token.decode()))

        return True
