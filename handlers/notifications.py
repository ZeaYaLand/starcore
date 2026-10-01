from telegram import Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.notification_service import get_notifications, mark_all_read
from services.player_service import get_or_create_player


async def notifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        items = get_notifications(session, player.id)
        if not items:
            await update.message.reply_text("🔔 Уведомлений пока нет.")
            return

        lines = ["🔔 УВЕДОМЛЕНИЯ\n"]
        for item in items:
            marker = "🔵" if not item.is_read else "⚪"
            lines.append(f"{marker} {item.title}\n{item.message}")
        await update.message.reply_text("\n\n".join(lines))


async def mark_notifications_read(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        changed = mark_all_read(session, player.id)
        await update.message.reply_text(f"🔔 Прочитано уведомлений: {changed}")
