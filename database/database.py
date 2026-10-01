from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    from database.game_state_models import PlayerGameState
    from database.models import Player
    from database.notification_models import Notification
    from database.profile_models import PlayerProfile
    from database.schema import SchemaVersion, apply_migrations
    from database.social_models import Group, GroupMember, Guild, GuildMember

    _ = (
        Player,
        PlayerProfile,
        Notification,
        PlayerGameState,
        Group,
        GroupMember,
        Guild,
        GuildMember,
        SchemaVersion,
    )
    apply_migrations()
