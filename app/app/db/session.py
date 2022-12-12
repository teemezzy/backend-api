from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from google.cloud.sql.connector import Connector, IPTypes
from app.core.logger_client import logger_client

logger = logger_client.getLogger(__name__)

engine = None
SessionLocal = None

if settings.ENVIRONMENT == "local":
    logger.info("Creating local db engine")
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"

    engine = create_engine(DATABASE_URL, echo=True)

    engine = create_engine(
        DATABASE_URL, pool_pre_ping=True, client_encoding="utf8"
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    logger.info("Creating cloud db engine")
    def getconn():
        with Connector() as connector:
            conn = connector.connect(
                settings.POSTGRES_INSTANCE_NAME, # Cloud SQL Instance Connection Name
                "pg8000",
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                db=settings.POSTGRES_DB,
                ip_type= IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
            )
        return conn

    SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL , creator=getconn
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
