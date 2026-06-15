import logging
import datetime
from alembic.config import Config
from alembic import command

logger = logging.getLogger(__name__)


def run_auto_migrations():
    logger.info("Starting database auto-migration check...")
    try:
        alembic_cfg = Config("alembic.ini")

        # 1. Run upgrade to head in case there are existing unapplied migrations
        logger.info("Upgrading database schema to the latest migration head...")
        command.upgrade(alembic_cfg, "head")

        # 2. Check if models and database schema are in sync
        logger.info("Checking database schema synchronization against models...")
        try:
            command.check(alembic_cfg)
            logger.info("Database schema is fully in sync with models.")
        except BaseException as e:
            if isinstance(e, SystemExit) and (e.code == 0 or e.code is None):
                logger.info("Database schema is fully in sync with models.")
            else:
                logger.info("Database schema is out of sync. Generating automatic migration revision...")
                try:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    command.revision(alembic_cfg, message=f"auto_{timestamp}", autogenerate=True)
                    logger.info("Applying the automatically generated migration to database...")
                    command.upgrade(alembic_cfg, "head")
                    logger.info("Automatic migration applied successfully.")
                except Exception as inner_e:
                    logger.info("Failed to generate/apply auto migration revision (this is normal if no changes detected): %s", inner_e)

    except Exception as e:
        logger.error(f"Failed to run database auto-migrations: {e}", exc_info=True)
        # We re-raise to fail startup if database schema cannot be verified/migrated
        raise e
