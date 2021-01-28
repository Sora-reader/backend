from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase

from models.models import Base, UserTable
from models.user import UserDB, User, UserCreate, UserUpdate
import settings


Base.metadata.create_all(settings.engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, settings.database, users)

app = FastAPI()

fastapi_users = FastAPIUsers(
    user_db,
    [settings.jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(settings.jwt_authentication),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/sign_up",
    tags=["auth"],
)


@app.on_event('startup')
async def startup():
    await settings.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await settings.database.disconnect()
