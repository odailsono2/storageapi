from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infra.bd import pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    yield
    await pool.close()
