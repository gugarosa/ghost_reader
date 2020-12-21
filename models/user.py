import datetime

from mongoengine import DateTimeField, Document, StringField


class User(Document):
    """A document that holds an user meta-information.

    """

    # User-related attributes
    username = StringField(required=True)
    password = StringField(required=True)

    # Date-related attributes
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
