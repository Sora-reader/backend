from fastapi_users.models import BaseUser, BaseUserCreate, BaseUserUpdate, BaseUserDB


class User(BaseUser):
    username: str
    pass


class UserCreate(BaseUserCreate):
    username: str
    pass


# Both classes below are currently not used in the API
class UserUpdate(User, BaseUserUpdate):
    # username: str
    pass


class UserDB(User, BaseUserDB):
    pass
