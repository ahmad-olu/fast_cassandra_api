import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Comment(Model):
    __keyspace__ = "geat_dev"
    author_id = columns.UUID(primary_key= True, required= True)
    id = columns.TimeUUID(primary_key= True, default=uuid.uuid1)
    author_username = columns.Text()
    author_profile_image_url = columns.Text()
    post_id = columns.UUID(primary_key= True,index = True, required= True)
    content = columns.Text(required= True)
    post_type = columns.Text(required= True)
    created_at = columns.DateTime(default= datetime.now())