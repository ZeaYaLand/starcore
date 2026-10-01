from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    from database.models import Player
    from database.profile_models import PlayerProfile
    from database.notification_models import Notification

    _ = (Player, PlayerProfile, Notification)
    Base.metadata.create_all(bind=engine)
