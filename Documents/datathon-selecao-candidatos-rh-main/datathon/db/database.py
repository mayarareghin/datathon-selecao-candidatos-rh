from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from datathon.core.settings import Settings

DATABASE_URL = Settings().DATABASE_URL  # vem do .env

# cria engine async
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# session factory para async
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# dependency para FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session