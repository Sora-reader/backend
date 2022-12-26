from typing import List

from apps.typesense_bind.schema import schema_name


def upsert_collection(client, data: List[dict]):
    return client.collections[schema_name].documents.import_(data, {"action": "upsert"})
