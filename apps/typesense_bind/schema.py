from apps.typesense_bind.client import get_ts_client

schema_name = "mangas"
schema = {
    "name": schema_name,
    "fields": [
        # There's only title since we only search by it
        # In reality there's more data in each doc
        {"name": "title", "type": "string", "locale": "ru"},
    ],
}


def upsert_schema():
    get_ts_client()
