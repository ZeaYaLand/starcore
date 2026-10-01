from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class PlayerProfile(Base):
    __tablename__ = "player_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    organism: Mapped[str] = mapped_column(String(100), default="Нулевой организм")
    strength: Mapped[int] = mapped_column(Integer, default=10)
    agility: Mapped[int] = mapped_column(Integer, default=10)
    vitality: Mapped[int] = mapped_column(Integer, default=10)
    intelligence: Mapped[int] = mapped_column(Integer, default=10)
    genome: Mapped[str] = mapped_column(Text, default="CORE-0001")
    achievements: Mapped[str] = mapped_column(Text, default="[]")
    inventory: Mapped[str] = mapped_column(Text, default="[]")
