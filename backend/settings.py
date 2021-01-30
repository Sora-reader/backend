import databases
from sqlalchemy import create_engine
from fastapi_users.authentication import JWTAuthentication

DATABASE_URL = "sqlite:///./db.sqlite3"

SECRET = "FMLKDFJKSDFJldsjcflsdfklsdjlf"

database = databases.Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)
