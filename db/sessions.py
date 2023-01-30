from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db.tables.transactions import Transaction

engine = create_engine(
    url=settings.sync_database_url,
    echo=settings.db_echo_log,
)

async_engine = create_async_engine(
    url=settings.async_database_url,
    echo=settings.db_echo_log,
    future=True,
)

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


def create_transaction():
    transaction = Transaction(amount=10, description="First transaction")

    with Session(engine) as session:
        session.add(transaction)
        session.commit()


def create_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    create_transaction()
