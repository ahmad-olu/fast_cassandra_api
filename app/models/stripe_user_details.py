import uuid
from fastapi import status, HTTPException
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class StripeCustomer(Model):
    __keyspace__ = "geat_dev"
    id = columns.UUID(primary_key= True, default=uuid.uuid1)
    stripe_id = columns.Text(primary_key= True)
    user_id = columns.Text(primary_key= True)
    user_username = columns.Text()
    user_profile_image_url = columns.Text()
    created_at = columns.DateTime(default= datetime.now())