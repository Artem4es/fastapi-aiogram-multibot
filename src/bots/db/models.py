from sqlalchemy import BigInteger, Column, DateTime, Integer, String, func

from src.bots.db.database import Base


class DBBot(Base):
    """
    - assistant_id: int ID of assistant in ALF DB
    - tg_id: int
    - token: str
    - created_at: DateTime (auto add)
    """

    __tablename__ = "bot"
    tg_id = Column(BigInteger, primary_key=True, unique=True)
    assistant_id = Column(Integer, nullable=False)
    token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
