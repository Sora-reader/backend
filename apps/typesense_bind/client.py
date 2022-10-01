import typesense
from django.conf import settings


def create_client(host, key, port=8108):
    return typesense.Client(
        {
            "nodes": [{"host": host, "port": port, "protocol": "http"}],
            "api_key": key,
            "connection_timeout_seconds": 2,
        }
    )


def get_ts_client():
    return settings.TS_CLIENT
