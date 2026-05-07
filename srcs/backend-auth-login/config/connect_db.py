# Standart
import os
from contextlib import asynccontextmanager

#Libraries
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Index, func
from fastapi import FastAPI, Depends
from uuid import uuid4
import logging
import asyncio
from datetime import datetime, timedelta, timezone

# Local files
from security import get_secret


db_user = os.getenv("DB_AUTH_USER")
db_port = os.getenv("DB_AUTH_PORT")
db_name = os.getenv("DB_AUTH_NAME")
db_password = get_secret(os.getenv("DB_AUTH_SECRETS"))

# logger = logging.getLogger("uvicorn.error")
# logger.info(f"DB_USER: {db_user}")
# logger.info(f"DB_NAME: {db_name}")
# logger.info(f"DB_PORT: {db_port}")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@db-auth:{db_port}/{db_name}"  # URL to connect to the postgres DB

engine = create_engine(DATABASE_URL)  # Create a pool of connexions ready to use

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # session rules manager for connexion with DB (add, commit, ...) and its behavior


class Base(DeclarativeBase):
    pass


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)

class SessionDB(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data = Column(JSONB, nullable=True)  # JSONB allows to construct a binary JSON (slower on writing but way faster for reading)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # func.now() is translated by ORM to SQL -> NOW() :
    																		# it garantees that only the DB server is involved in the timing and not python app server

    # Index composite pour les lookups rapides
    __table_args__ = (
        Index('idx_session_id_expires', 'id', 'expires_at'),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    async def _cleanup_loop():
        # loop to check every 3600 seconds and clean the expired sessions 
        while True:
            await asyncio.sleep(3600) # tells to the server it will wait 1 hour before doing its job after, and the server remains accessible anyway
            cleanup_session = SessionLocal()
            try:
                try:
                    cleanup_session.query(SessionDB).filter(SessionDB.expires_at < datetime.now(timezone.utc)).delete()
                    cleanup_session.commit()
                except Exception:
                    cleanup_session.rollback()
            finally:
                cleanup_session.close()

    cleanup_task = asyncio.create_task(_cleanup_loop())
    try:
        yield
    finally:
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass


auth = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()  # ouvre le panier
    try:
        yield db  # donne le panier à la route
    finally:
        db.close()