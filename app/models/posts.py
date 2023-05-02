import uuid
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Post(Model):
    __keyspace__ = "geat_dev"
    author_id = columns.UUID(primary_key= True, required= True)
    id = columns.TimeUUID(primary_key= True, default=uuid.uuid1)
    author_username = columns.Text()
    author_profile_image_url = columns.Text()
    title = columns.Text(index = True, required= True)
    sub_title = columns.Text()
    url_path = columns.Text()
    publish = columns.Boolean(default= True)
    can_re_imagine = columns.Boolean(default= False)
    can_comment = columns.Boolean(default= True)
    images_url = columns.List(value_type=columns.Text())
    content = columns.Text(required= True)
    post_type = columns.Text()
    created_at = columns.DateTime(default= datetime.now())