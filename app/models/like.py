import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Like(Model):
    __keyspace__ = "geat_dev"
    id = columns.UUID(primary_key= True, default=uuid.uuid1)
    post_id = columns.UUID(primary_key= True,index = True, required= True)
    liked_by = columns.UUID(primary_key= True,index = True, required= True)
    created_at = columns.DateTime(default= datetime.now())