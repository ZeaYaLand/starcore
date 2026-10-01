from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from services.player_service import get_or_create_player, add_xp, spend_energy, add_credits
from services.profile_service import get_or_create_profile
from game.locations import LOCATIONS
from game.events import EventService


def hub_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton("🎮 Игра", callback_data="hub:game"), InlineKeyboardButton("🧬 Геном", callback_data="hub:genome")],
        [InlineKeyboardButton("⚔️ Бой", callback_data="hub:combat"), InlineKeyboardButton("🗺️ Исследование", callback_data="hub:explore")],
        [InlineKeyboardButton("🎒 Инвентарь", callback_data="hub:inventory"), InlineKeyboardButton("🔨 Крафт", callback_data="hub:craft")],
        [InlineKeyboardButton("🧫 Эволюция", callback_data="hub:evolution"), InlineKeyboardButton("🏆 Достижения", callback_data="hub:achievements")],
        [InlineKeyboardButton("👥 Социальное", callback_data="hub:social"), InlineKeyboardButton("🏰 Гильдии", callback_data="hub:guilds")],
        [InlineKeyboardButton("📈 Рейтинг", callback_data="hub:ranking"), InlineKeyboardButton("💰 Экономика", callback_data="hub:economy")],
        [InlineKeyboardButton("📅 Ежедневное", callback_data="hub:daily"), InlineKeyboardButton("🌍 События", callback_data="hub:events")],
        [InlineKeyboardButton("🛒 Магазин", callback_data="hub:shop"), InlineKeyboardButton("⚡ Способности", callback_data="hub:abilities")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="hub:menu")],
    ]
    return InlineKeyboardMarkup(rows)


def hub_text(player, profile) -> str:
    return (
        "🌌 STARCORE\n\n"
        f"🧫 {profile.organism}\n"
        f"🏆 Уровень {player.level} • XP {player.xp}\n"
        f"⚡ Энергия {player.energy}/100\n"
        f"🪙 {player.credits} • 💎 {player.crystals}\n\n"
        "Все основные системы STARCORE собраны здесь."
    )


async def hub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return
    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile = get_or_create_profile(session, player.id)
        await message.reply_text(hub_text(player, profile), reply_markup=hub_keyboard())


async def hub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    await query.answer()
    message = query.message
    user = update.effective_user
    if message is None or user is None:
        return
    action = query.data

    if action == "hub:menu":
        from handlers.menu import main_menu_keyboard
        await message.reply_text("🎮 Главное меню STARCORE", reply_markup=main_menu_keyboard())
        return
    if action == "hub:game":
        from handlers.game import game
        await game(update, context)
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile = get_or_create_profile(session, player.id)

        if action == "hub:explore":
            lines = ["🗺️ ИССЛЕДОВАНИЕ\n"]
            for loc in LOCATIONS:
                lines.append(f"• {loc.name} — ⚡{loc.energy_cost} — опасность {loc.danger}%")
            lines.append("\nВыбери локацию командой /explore <id>.")
            await message.reply_text("\n".join(lines), reply_markup=hub_keyboard())
        elif action == "hub:genome":
            await message.reply_text(f"🧬 ГЕНОМ\n\nКод: {profile.genome}\nОрганизм: {profile.organism}", reply_markup=hub_keyboard())
        elif action == "hub:inventory":
            await message.reply_text(f"🎒 ИНВЕНТАРЬ\n\n{profile.inventory}", reply_markup=hub_keyboard())
        elif action == "hub:achievements":
            await message.reply_text(f"🏆 ДОСТИЖЕНИЯ\n\n{profile.achievements}", reply_markup=hub_keyboard())
        elif action == "hub:evolution":
            await message.reply_text("🧫 ЭВОЛЮЦИЯ\n\nСистема эволюции подключена к игровому ядру. Следующий шаг — безопасно привязать изменение организма к сохранению в БД.", reply_markup=hub_keyboard())
        elif action in {"hub:combat", "hub:craft", "hub:social", "hub:guilds", "hub:ranking", "hub:economy", "hub:daily", "hub:events", "hub:shop", "hub:abilities"}:
            names = {
                "hub:combat":"⚔️ БОЙ", "hub:craft":"🔨 КРАФТ", "hub:social":"👥 СОЦИАЛЬНОЕ", "hub:guilds":"🏰 ГИЛЬДИИ",
                "hub:ranking":"📈 РЕЙТИНГ", "hub:economy":"💰 ЭКОНОМИКА", "hub:daily":"📅 ЕЖЕДНЕВНОЕ", "hub:events":"🌍 СОБЫТИЯ",
                "hub:shop":"🛒 МАГАЗИН", "hub:abilities":"⚡ СПОСОБНОСТИ"
            }
            await message.reply_text(f"{names[action]}\n\nСистема присутствует в STARCORE backend. Сейчас подключаем её Telegram-интерфейс к реальному состоянию игрока.", reply_markup=hub_keyboard())
