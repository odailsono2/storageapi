from psycopg_pool import AsyncConnectionPool

DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

pool = AsyncConnectionPool(conninfo=DATABASE_URL, open=False)


async def get_db_connection() -> AsyncConnectionPool:
    async with pool.connection() as conn:
        yield conn
