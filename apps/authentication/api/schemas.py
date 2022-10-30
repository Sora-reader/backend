from ninja import Schema


class CredentialsIn(Schema):
    username: str
    password: str


class SessionOut(Schema):
    session: str
