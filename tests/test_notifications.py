from database.database import Base, SessionLocal, engine
from services.notification_service import (
    create_notification,
    get_notifications,
    mark_all_read,
    mark_read,
    unread_count,
)
from services.player_service import get_or_create_player


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def player(session, telegram_id=57001):
    return get_or_create_player(session, telegram_id, "notification_user")


def test_create_and_read_notifications():
    with SessionLocal() as session:
        p = player(session)
        item = create_notification(session, p.id, "Новая награда", "Ты получил 25 XP", "reward")

        items = get_notifications(session, p.id)

        assert len(items) == 1
        assert items[0].id == item.id
        assert items[0].title == "Новая награда"
        assert items[0].is_read is False
        assert unread_count(session, p.id) == 1


def test_notifications_are_private_to_player():
    with SessionLocal() as session:
        p1 = player(session, 57002)
        p2 = player(session, 57003)
        create_notification(session, p1.id, "A", "Only player one")
        create_notification(session, p2.id, "B", "Only player two")

        assert [n.message for n in get_notifications(session, p1.id)] == ["Only player one"]
        assert [n.message for n in get_notifications(session, p2.id)] == ["Only player two"]


def test_mark_read_and_mark_all_read():
    with SessionLocal() as session:
        p = player(session, 57004)
        first = create_notification(session, p.id, "A", "One")
        create_notification(session, p.id, "B", "Two")
        assert unread_count(session, p.id) == 2

        assert mark_read(session, p.id, first.id) is True
        assert unread_count(session, p.id) == 1
        assert mark_all_read(session, p.id) == 1
        assert unread_count(session, p.id) == 0


def test_invalid_notification_data_is_rejected():
    with SessionLocal() as session:
        p = player(session, 57005)
        try:
            create_notification(session, p.id, "", "message")
            assert False
        except ValueError:
            pass

        try:
            get_notifications(session, p.id, 0)
            assert False
        except ValueError:
            pass
