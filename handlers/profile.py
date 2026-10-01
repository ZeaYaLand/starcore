from telegram import Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.player_service import get_or_create_player
from services.profile_service import get_or_create_profile, profile_data


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.effective_message
    if user is None or message is None:
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile_record = get_or_create_profile(session, player.id)
        data = profile_data(profile_record)
        achievements = data["achievements"]
        inventory = data["inventory"]
        characteristics = data["characteristics"]

        await message.reply_text(
            "🧬 ПРОФИЛЬ ОРГАНИЗМА\n\n"
            f"👤 Имя: @{player.username or 'unknown'}\n"
            f"🧫 Организм: {data['organism']}\n"
            f"🧬 Геном: {data['genome']}\n\n"
            "🧪 БИОПРОФИЛЬ\n"
            f"💪 Сила: {characteristics['strength']}\n"
            f"🏃 Ловкость: {characteristics['agility']}\n"
            f"❤️ Живучесть: {characteristics['vitality']}\n"
            f"🧠 Интеллект: {characteristics['intelligence']}\n\n"
            "🏅 СОБРАННЫЕ ДАННЫЕ\n"
            f"🏆 Достижения: {len(achievements)}\n"
            f"🎒 Предметы: {len(inventory)}\n\n"
            "🔬 Профиль показывает твою сущность, геном и состояние организма."
        )
