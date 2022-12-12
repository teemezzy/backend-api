import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.core.logger_client import logger_client

logger = logger_client.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
