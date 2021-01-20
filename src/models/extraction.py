import datetime

from mongoengine import DateTimeField, Document, StringField


class Extraction(Document):
    """A document that holds an extraction meta-information.

    """

    # Extract-related attributes
    text = StringField()
    url = StringField(required=True)
    local_path = StringField()
    status = StringField(required=True)

    # Date-related attributes
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
