from sqlalchemy import ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class PlayerGameState(Base):
    __tablename__ = "player_game_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), unique=True, index=True)
    genome: Mapped[dict] = mapped_column(JSON, default=dict)
    inventory: Mapped[dict] = mapped_column(JSON, default=dict)
    equipment: Mapped[dict] = mapped_column(JSON, default=dict)
    progression: Mapped[dict] = mapped_column(JSON, default=dict)
    quests: Mapped[dict] = mapped_column(JSON, default=dict)
    daily: Mapped[dict] = mapped_column(JSON, default=dict)
    exploration: Mapped[dict] = mapped_column(JSON, default=dict)
    combat: Mapped[dict] = mapped_column(JSON, default=dict)
    abilities: Mapped[dict] = mapped_column(JSON, default=dict)
    effects: Mapped[dict] = mapped_column(JSON, default=dict)
    economy: Mapped[dict] = mapped_column(JSON, default=dict)
