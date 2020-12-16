import datetime

from mongoengine import DateTimeField, Document, ReferenceField, StringField

from models.extraction import Extraction


class Detection(Document):
    """A document that holds a detection meta-information.

    """

    # Detect-related attributes
    local_path = StringField()
    extraction = ReferenceField(Extraction)
    status = StringField(required=True)

    # Date-related attributes
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
