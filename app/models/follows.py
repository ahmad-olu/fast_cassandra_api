import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Follower(Model):
    __keyspace__ = "geat_dev"
    id = columns.UUID(primary_key= True, default=uuid.uuid1)
    user_id = columns.UUID(index = True, required= True)
    followers = columns.UUID(index = True, required= True)
    created_at = columns.DateTime(default= datetime.now())

class Following(Model):
    __keyspace__ = "geat_dev"
    id = columns.UUID(primary_key= True, default=uuid.uuid1)
    following = columns.UUID(primary_key= True,index = True, required= True)
    user_id = columns.UUID(index = True, required= True)
    created_at = columns.DateTime(default= datetime.now())