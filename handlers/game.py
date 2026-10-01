from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.player_service import get_or_create_player
from services.profile_service import get_or_create_profile


def game_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Действие", callback_data="game:action"), InlineKeyboardButton("🧬 Геном", callback_data="game:genome")],
        [InlineKeyboardButton("💪 Характеристики", callback_data="game:stats"), InlineKeyboardButton("🎒 Инвентарь", callback_data="game:inventory")],
        [InlineKeyboardButton("🔙 Меню", callback_data="game:menu")],
    ])


def game_text(player, profile) -> str:
    return (
        "🎮 STARCORE — ИГРА\n\n"
        f"🧫 Организм: {profile.organism}\n"
        f"🏆 Уровень: {player.level}\n"
        f"✨ XP: {player.xp}\n"
        f"⚡ Энергия: {player.energy}/100\n\n"
        "Выбери, что делать дальше."
    )


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return
    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile = get_or_create_profile(session, player.id)
        await message.reply_text(game_text(player, profile), reply_markup=game_keyboard())


async def game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    message = query.message
    user = update.effective_user
    if message is None or user is None:
        return
    action = query.data
    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile = get_or_create_profile(session, player.id)
        if action == "game:action":
            if player.energy <= 0:
                await message.reply_text("⚡ Энергия закончилась. Отдохни и попробуй снова.")
                return
            player.energy -= 1
            player.xp += 10
            session.commit()
            await message.reply_text("⚡ Действие выполнено! +10 XP, -1 энергия.", reply_markup=game_keyboard())
        elif action == "game:genome":
            await message.reply_text(f"🧬 Твой геном: {profile.genome}", reply_markup=game_keyboard())
        elif action == "game:stats":
            await message.reply_text(
                "💪 Характеристики\n\n"
                f"Сила: {profile.strength}\nЛовкость: {profile.agility}\n"
                f"Живучесть: {profile.vitality}\nИнтеллект: {profile.intelligence}",
                reply_markup=game_keyboard(),
            )
        elif action == "game:inventory":
            await message.reply_text("🎒 Инвентарь пока пуст.", reply_markup=game_keyboard())
        elif action == "game:menu":
            from handlers.menu import main_menu_keyboard
            await message.reply_text("🎮 Главное меню STARCORE", reply_markup=main_menu_keyboard())
