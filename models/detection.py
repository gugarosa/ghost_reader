import datetime

from mongoengine import DateTimeField, Document, StringField


class Detection(Document):
    """An document that holds an detection meta-information.

    """

    # Detect-related attributes
    status = StringField(required=True)

    # Date-related attributes
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
