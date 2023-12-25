from datetime import datetime
from typing import Annotated

from sqlalchemy import text, BigInteger, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from src.bots.db.database import Base
from src.config import Settings

settings = Settings()


intpk = Annotated[int, mapped_column(primary_key=True)]
# created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# updated_at = Annotated[datetime, mapped_column(DateTime(), server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]


class BotORM(Base):
    __tablename__ = "assistant_bot"
    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    token: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    prompt: Mapped[str]
    engine: Mapped[str] = mapped_column(default=settings.default_engine, server_default=settings.default_engine)
    temperature: Mapped[
        float] = mapped_column(default=settings.default_temperature, server_default=str(settings.default_temperature))
    created_at = mapped_column(DateTime(), default=datetime.utcnow(), server_default=text("TIMEZONE('utc', now())"), nullable=False)
    updated_at = mapped_column(DateTime(), server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow, nullable=False)

