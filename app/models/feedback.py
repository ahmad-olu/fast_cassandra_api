import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Feedback(Model):
    __keyspace__ = "geat_dev"
    author_id = columns.UUID(primary_key= True, required= True)
    id = columns.TimeUUID(primary_key= True, default=uuid.uuid1)
    author_username = columns.Text()
    author_email = columns.Text()
    image_url = columns.Text()
    content = columns.Text()
    created_at = columns.DateTime(default= datetime.now())