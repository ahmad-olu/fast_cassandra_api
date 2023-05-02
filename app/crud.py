from cassandra.cqlengine.management import sync_table
from .db import get_session
from .models.users import User


session = get_session()
sync_table(User)

def create_entry(data:dict):
    return User.create(**data)