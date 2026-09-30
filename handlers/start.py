from telegram import Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.player_service import get_or_create_player
from handlers.menu import main_menu_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)

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
