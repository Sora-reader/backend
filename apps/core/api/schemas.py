from ninja import Schema


class MessageSchema(Schema):
    message: str


class ErrorSchema(Schema):
    error: str
