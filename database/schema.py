from sqlalchemy import Integer, select
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base, engine


CURRENT_SCHEMA_VERSION = 2


class SchemaVersion(Base):
    __tablename__ = "schema_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[int] = mapped_column(Integer, unique=True, index=True)


def apply_migrations() -> int:
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        existing = connection.execute(
            select(SchemaVersion).where(SchemaVersion.version == CURRENT_SCHEMA_VERSION)
        ).first()
        if existing is None:
            connection.execute(
                SchemaVersion.__table__.insert().values(version=CURRENT_SCHEMA_VERSION)
            )
    return CURRENT_SCHEMA_VERSION
