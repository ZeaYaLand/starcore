from sqlalchemy import func, select

from database.notification_models import Notification


def create_notification(session, player_id: int, title: str, message: str, kind: str = "system") -> Notification:
    if player_id <= 0:
        raise ValueError("player_id must be positive")
    if not title.strip() or not message.strip():
        raise ValueError("title and message are required")

    notification = Notification(
        player_id=player_id,
        title=title.strip(),
        message=message.strip(),
        kind=kind.strip() or "system",
    )
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


def get_notifications(session, player_id: int, limit: int = 20) -> list[Notification]:
    if player_id <= 0:
        raise ValueError("player_id must be positive")
    if limit <= 0:
        raise ValueError("limit must be positive")

    return list(
        session.scalars(
            select(Notification)
            .where(Notification.player_id == player_id)
            .order_by(Notification.created_at.desc(), Notification.id.desc())
            .limit(limit)
        )
    )


def unread_count(session, player_id: int) -> int:
    if player_id <= 0:
        raise ValueError("player_id must be positive")
    return int(
        session.scalar(
            select(func.count(Notification.id)).where(
                Notification.player_id == player_id,
                Notification.is_read.is_(False),
            )
        )
        or 0
    )


def mark_read(session, player_id: int, notification_id: int) -> bool:
    notification = session.scalar(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.player_id == player_id,
        )
    )
    if notification is None:
        return False
    notification.is_read = True
    session.commit()
    return True


def mark_all_read(session, player_id: int) -> int:
    notifications = get_notifications(session, player_id, limit=1000)
    changed = 0
    for notification in notifications:
        if not notification.is_read:
            notification.is_read = True
            changed += 1
    session.commit()
    return changed
