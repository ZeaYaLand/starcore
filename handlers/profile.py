from telegram import Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.player_service import get_or_create_player, xp_required_for_level
from services.profile_service import get_or_create_profile, profile_data


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile_record = get_or_create_profile(session, player.id)
        data = profile_data(profile_record)
        xp_needed = xp_required_for_level(player.level)
        characteristics = data["characteristics"]
        achievements = data["achievements"]
        inventory = data["inventory"]

        await update.message.reply_text(
            "🧬 ТВОЙ STARCORE ПРОФИЛЬ\n\n"
            f"👤 @{player.username or 'unknown'}\n"
            f"🧫 Организм: {data['organism']}\n"
            f"🏆 Уровень: {player.level}\n"
            f"✨ XP: {player.xp}/{xp_needed}\n"
            f"🪙 Кредиты: {player.credits}\n"
            f"💎 Кристаллы: {player.crystals}\n"
            f"⚡ Энергия: {player.energy}/100\n\n"
            "📊 Характеристики:\n"
            f"💪 Сила: {characteristics['strength']}\n"
            f"🏃 Ловкость: {characteristics['agility']}\n"
            f"❤️ Живучесть: {characteristics['vitality']}\n"
            f"🧠 Интеллект: {characteristics['intelligence']}\n\n"
            f"🧬 Геном: {data['genome']}\n"
            f"🏅 Достижений: {len(achievements)}\n"
            f"🎒 Предметов: {len(inventory)}"
        )
