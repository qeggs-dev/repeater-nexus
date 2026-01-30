from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncIterator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield