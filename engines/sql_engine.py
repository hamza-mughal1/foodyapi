from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from utilities.settings import setting

# PostgreSQL connection string for async support
SQLALCHEMY_DATABASE_URL = (
    f"{setting.db}+asyncpg://{setting.db_username}:{setting.db_password}"
    f"@{setting.db_host}:{setting.db_port}/{setting.db_name}"
)

# Main async database engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# Async session object to create sessions to the database on each request
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base object to manage SQLAlchemy ORM and to create tables
Base = declarative_base()

# Async get_db function to create a generator object for session
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
