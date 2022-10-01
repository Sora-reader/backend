from apps.typesense_bind.client import get_ts_client

schema_name = "mangas"
schema = {
    "name": schema_name,
    "fields": [
        {"name": "title", "type": "string", "locale": "ru"},
        {"name": "alt_title", "type": "string"},
    ],
}


def upsert_schema():
    get_ts_client()
