from fastapi import FastAPI, status

from api.router import router
from core.config import settings
from db.sessions import create_tables

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {"Say": "Hello!"}


@app.get("/init_tables", status_code=status.HTTP_200_OK, name="init_tables")
async def init_tables():
    create_tables()
