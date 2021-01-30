import uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from settings import engine, jwt_authentication, database
from models.models import Base, UserTable
from models.user import UserDB, User, UserCreate, UserUpdate

app = FastAPI()

# Creating SQLAlchemy engine to define tables
Base.metadata.create_all(engine)

# Creating database adapter
users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)


# Wiring a database adapter  and auth Classes
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
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
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)