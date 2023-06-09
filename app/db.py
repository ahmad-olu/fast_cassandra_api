import pathlib
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection
from app import config



settings = config.get_settings()

def bundle_location():
    if settings.environment_representation == 0:
        return str(BASE_DIR / "ignored" / "dev" / 'connect.zip')
    elif settings.environment_representation == 1:
        return str(BASE_DIR / "ignored" / "prod" / 'connect.zip')
    else:
        return str(BASE_DIR / "ignored" / "dev" / 'connect.zip')

BASE_DIR = pathlib.Path(__file__).parent 
CLUSTER_BUNDLE = bundle_location()


def get_cluster():
    cloud_config= {
         'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(settings.astra_db_client_id, settings.astra_db_client_secret) 
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster


def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session


# session = get_session()
# row = session.execute("select release_version from system.local").one()
# if row:
#       print(row[0])
# else:
#       print("An error occurred.")