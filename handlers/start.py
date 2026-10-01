import logging

from telegram import Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.player_service import get_or_create_player
from handlers.menu import main_menu_keyboard


logger = logging.getLogger("starcore.start")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        logger.warning("/start received without effective_user or message")
        return

    logger.info("/start received: user_id=%s username=%r", user.id, user.username)

    try:
        with SessionLocal() as session:
            player = get_or_create_player(session, user.id, user.username)

        logger.info("/start player ready: user_id=%s player_id=%s level=%s", user.id, player.id, player.level)

        await update.message.reply_text(
            "🌌 STARCORE\n\n"
            "Добро пожаловать в игру.\n\n"
            f"🧬 Уровень: {player.level}\n"
            f"🪙 Кредиты: {player.credits}\n"
            f"💎 Кристаллы: {player.crystals}\n"
            f"⚡ Энергия: {player.energy}\n\n"
            "Выберите раздел в меню ниже.",
            reply_markup=main_menu_keyboard(),
        )
        logger.info("/start reply sent: user_id=%s", user.id)
    except Exception:
        logger.exception("/start failed: user_id=%s", user.id)
        raise
