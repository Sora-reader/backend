import typesense
from django.conf import settings


def create_client(host, key, protocol, port=8108):
    return typesense.Client(
        {
            "nodes": [
                {
                    "host": host,
                    "port": port if protocol != "https" else "443",
                    "protocol": "http",
                },
            ],
            "api_key": key,
            "connection_timeout_seconds": 10,
        }
    )


def get_ts_client():
    return settings.TS_CLIENT
