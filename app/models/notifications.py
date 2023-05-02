import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Notification(Model):
    __keyspace__ = "geat_dev"
    owner_id = columns.Text(primary_key= True,index = True, required= True)
    id = columns.UUID(primary_key= True, default=uuid.uuid1)
    author = columns.Text(index = True, required= True)
    message = columns.Text()
    notification_type = columns.Text(required= True)
    created_at = columns.DateTime(default= datetime.now())