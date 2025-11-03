"""
Database Connection Manager
Handles connections with pooling, error handling, and health checks
"""

import os
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import logging

from .models import Base

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration with environment variable support."""

    def __init__(self):
        self.database_url = os.getenv(
            'DATABASE_URL',
            'sqlite:///pokemon_enterprise.db'
        )
        self.pool_size = int(os.getenv('DB_POOL_SIZE', '5'))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '10'))
        self.pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', '30'))
        self.echo = os.getenv('DB_ECHO', 'False').lower() == 'true'

    def get_engine_kwargs(self):
        """Get engine configuration based on database type."""
        kwargs = {
            'echo': self.echo,
            'future': True
        }

        # Only add pooling for PostgreSQL (not SQLite)
        if not self.database_url.startswith('sqlite'):
            kwargs.update({
                'poolclass': pool.QueuePool,
                'pool_size': self.pool_size,
                'max_overflow': self.max_overflow,
                'pool_timeout': self.pool_timeout,
                'pool_pre_ping': True,
            })

        return kwargs


class DatabaseManager:
    """
    Manages database connections, sessions, and lifecycle.
    Implements singleton pattern for connection pooling.
    """

    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._engine is None:
            self.config = DatabaseConfig()
            self._initialize_engine()
            self._initialize_session_factory()
            self._setup_event_listeners()

    def _initialize_engine(self):
        """Create database engine with configuration."""
        try:
            engine_kwargs = self.config.get_engine_kwargs()
            self._engine = create_engine(
                self.config.database_url,
                **engine_kwargs
            )
            logger.info(
                f"✅ Database engine created: "
                f"{self.config.database_url.split('://')[0]}"
            )
        except Exception as e:
            logger.error(f"❌ Failed to create engine: {e}")
            raise

    def _initialize_session_factory(self):
        """Create session factory."""
        self._SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    def _setup_event_listeners(self):
        """Setup SQLAlchemy event listeners for monitoring."""

        @event.listens_for(self._engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            logger.debug("Database connection established")

        @event.listens_for(self._engine, "close")
        def receive_close(dbapi_conn, connection_record):
            logger.debug("Database connection closed")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions.
        Automatically handles commit/rollback and cleanup.

        Usage:
            with db_manager.get_session() as session:
                result = session.query(Pokemon).all()
        """
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"❌ Database error: {e}")
            raise
        finally:
            session.close()

    def create_tables(self):
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=self._engine)
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            raise

    def drop_tables(self):
        """Drop all database tables (use with caution!)."""
        try:
            Base.metadata.drop_all(bind=self._engine)
            logger.warning("⚠️  All database tables dropped")
        except Exception as e:
            logger.error(f"❌ Failed to drop tables: {e}")
            raise

    def health_check(self) -> bool:
        """
        Check database connection health.
        Returns True if connection is healthy, False otherwise.
        """
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
            logger.info("✅ Database health check passed")
            return True
        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            return False

    @property
    def engine(self):
        """Get the SQLAlchemy engine."""
        return self._engine

    def get_connection_info(self) -> dict:
        """Get current database connection information."""
        return {
            'database_type': self.config.database_url.split('://')[0],
            'pool_size': self.config.pool_size,
            'max_overflow': self.config.max_overflow,
            'echo': self.config.echo,
        }


# Global database manager instance
db_manager = DatabaseManager()


# Convenience functions
def get_session() -> Generator[Session, None, None]:
    """Get database session (convenience function)."""
    return db_manager.get_session()


def init_database():
    """Initialize database (create tables)."""
    db_manager.create_tables()


def check_database_health() -> bool:
    """Check database health (convenience function)."""
    return db_manager.health_check()


if __name__ == "__main__":
    # Test database connection
    print("🔧 Testing database connection...")

    # Create tables
    init_database()

    # Health check
    if check_database_health():
        print("✅ Database is ready!")

        # Print connection info
        info = db_manager.get_connection_info()
        print(f"\n📊 Connection Info:")
        for key, value in info.items():
            print(f"  - {key}: {value}")
    else:
        print("❌ Database connection failed!")
