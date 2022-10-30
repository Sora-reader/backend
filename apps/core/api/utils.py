from apps.core.api.schemas import ErrorSchema, MessageSchema


def sora_schema(schema):
    return {200: schema, 400: ErrorSchema, 425: MessageSchema}
