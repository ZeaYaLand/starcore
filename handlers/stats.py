from telegram import Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.player_service import get_or_create_player
from services.profile_service import get_or_create_profile
from services.statistics_service import build_statistics


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.effective_message
    if user is None or message is None:
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile = get_or_create_profile(session, player.id)
        data = build_statistics(player, profile)

        await message.reply_text(
            "📊 АНАЛИТИКА STARCORE\n\n"
            "🚀 ПРОГРЕСС\n"
            f"🏆 Уровень: {data['level']}\n"
            f"✨ XP: {data['xp']}/{data['xp_required']}\n"
            f"📈 Заполнение уровня: {data['xp_progress_percent']:.0f}%\n\n"
            "⚡ РЕСУРСЫ\n"
            f"🪙 Кредиты: {data['credits']}\n"
            f"💎 Кристаллы: {data['crystals']}\n"
            f"⚡ Энергия: {data['energy']}/{data['max_energy']}\n\n"
            "🧠 БОЕВОЙ ПОТЕНЦИАЛ\n"
            f"💪 Сумма характеристик: {data['total_attributes']}\n"
            f"🏅 Открыто достижений: {data['achievements_unlocked']}\n\n"
            "🎒 КОЛЛЕКЦИОННЫЙ ПРОГРЕСС\n"
            f"📦 Предметов собрано: {data['inventory_items']}\n\n"
            "📡 Этот раздел показывает динамику развития и ресурсы, а не описание твоего организма."
        )
