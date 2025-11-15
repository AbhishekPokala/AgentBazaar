from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings

# Convert postgresql:// to postgresql+asyncpg:// for async support
# Handle sslmode parameter: asyncpg expects boolean ssl arg instead
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Parse and remove sslmode from query string, preserve other params
connect_args = {}
if "?sslmode=" in database_url or "&sslmode=" in database_url:
    # asyncpg needs ssl=True instead of sslmode=require
    connect_args["ssl"] = True
    # Remove sslmode from URL while preserving other query params
    import re
    database_url = re.sub(r'[?&]sslmode=[^&]*', '', database_url)
    # Fix double '?' or trailing '?'
    database_url = re.sub(r'\?&', '?', database_url)
    database_url = re.sub(r'\?$', '', database_url)

engine = create_async_engine(
    database_url,
    echo=settings.LOG_LEVEL == "DEBUG",
    pool_pre_ping=True,
    connect_args=connect_args,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create declarative base
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency for getting async database session.
    Usage: db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
