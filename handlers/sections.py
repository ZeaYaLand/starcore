import json
from typing import Any

from sqlalchemy import func, select
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database.database import SessionLocal
from database.game_state_models import PlayerGameState
from database.models import Player
from database.profile_models import PlayerProfile
from database.social_models import GuildMember, GroupMember
from services.player_service import get_or_create_player
from services.profile_service import get_or_create_profile


SECTION_LABELS = {
    "inventory": "🎒 Инвентарь",
    "missions": "🎯 Миссии",
    "achievements": "🏆 Достижения",
    "ranking": "🏅 Рейтинг",
    "social": "👥 Сообщество",
    "guild": "🛡 Гильдия",
    "trading": "💱 Торговля",
    "shop": "🛒 Магазин",
    "systems": "🌌 Системы",
}


def sections_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [(SECTION_LABELS["inventory"], "section:inventory"), (SECTION_LABELS["missions"], "section:missions")],
        [(SECTION_LABELS["achievements"], "section:achievements"), (SECTION_LABELS["ranking"], "section:ranking")],
        [(SECTION_LABELS["social"], "section:social"), (SECTION_LABELS["guild"], "section:guild")],
        [(SECTION_LABELS["trading"], "section:trading"), (SECTION_LABELS["shop"], "section:shop")],
        [(SECTION_LABELS["systems"], "section:systems")],
        [("🔙 Главное меню", "section:menu")],
    ]
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text, callback_data=data) for text, data in row] for row in rows]
    )


def _json_list(value: str | None) -> list[Any]:
    try:
        parsed = json.loads(value or "[]")
    except (TypeError, json.JSONDecodeError):
        return []
    return parsed if isinstance(parsed, list) else []


def _json_dict(value: dict | None) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _state(session, player_id: int) -> PlayerGameState | None:
    return session.scalar(select(PlayerGameState).where(PlayerGameState.player_id == player_id))


def _section_text(session, player: Player, profile: PlayerProfile, key: str) -> str:
    state = _state(session, player.id)

    if key == "inventory":
        profile_items = _json_list(profile.inventory)
        state_items = list((_json_dict(state.inventory) if state else {}).get("items", []))
        items = state_items or profile_items
        if not items:
            return "🎒 ИНВЕНТАРЬ\n\nИнвентарь пока пуст.\n\nПредметы будут появляться после игровых действий."
        lines = ["🎒 ИНВЕНТАРЬ", ""]
        for item in items[:20]:
            if isinstance(item, dict):
                lines.append(f"• {item.get('name', 'Предмет')} ×{item.get('quantity', 1)}")
            else:
                lines.append(f"• {item}")
        return "\n".join(lines)

    if key == "missions":
        quests = _json_dict(state.quests if state else None)
        active = quests.get("active", [])
        completed = quests.get("completed", 0)
        lines = ["🎯 МИССИИ", "", f"Выполнено: {completed}"]
        if active:
            lines.append("\nАктивные:")
            for quest in active[:10]:
                if isinstance(quest, dict):
                    lines.append(f"• {quest.get('name', 'Миссия')} — {quest.get('progress', 0)}/{quest.get('target', '?')}")
                else:
                    lines.append(f"• {quest}")
        else:
            lines.append("\nАктивных миссий пока нет.")
        return "\n".join(lines)

    if key == "achievements":
        achievements = _json_list(profile.achievements)
        if not achievements:
            return "🏆 ДОСТИЖЕНИЯ\n\nПока нет открытых достижений.\nВыполняй игровые действия, чтобы открыть первые."
        return "🏆 ДОСТИЖЕНИЯ\n\n" + "\n".join(f"• {item}" for item in achievements[:30])

    if key == "ranking":
        leaders = session.scalars(
            select(Player).order_by(Player.level.desc(), Player.xp.desc(), Player.credits.desc()).limit(10)
        ).all()
        lines = ["🏅 РЕЙТИНГ STARCORE", ""]
        for position, leader in enumerate(leaders, 1):
            name = f"@{leader.username}" if leader.username else f"Игрок {leader.telegram_id}"
            marker = "⭐" if leader.id == player.id else "•"
            lines.append(f"{position}. {marker} {name} — ур. {leader.level}, XP {leader.xp}")
        return "\n".join(lines)

    if key == "social":
        groups = session.scalar(select(func.count(GroupMember.id)).where(GroupMember.player_id == player.id)) or 0
        guilds = session.scalar(select(func.count(GuildMember.id)).where(GuildMember.player_id == player.id)) or 0
        return (
            "👥 СООБЩЕСТВО\n\n"
            f"Группы: {groups}\n"
            f"Гильдии: {guilds}\n\n"
            "Социальные механики STARCORE собраны в одном разделе."
        )

    if key == "guild":
        memberships = session.scalar(select(func.count(GuildMember.id)).where(GuildMember.player_id == player.id)) or 0
        return (
            "🛡 ГИЛЬДИЯ\n\n"
            f"Членство: {memberships}\n"
            "Очки гильдии отображаются после вступления.\n\n"
            "Здесь будет управление составом, очками и совместным прогрессом."
        )

    if key == "trading":
        return (
            "💱 ТОРГОВЛЯ\n\n"
            f"🪙 Кредиты: {player.credits}\n"
            f"💎 Кристаллы: {player.crystals}\n\n"
            "Раздел торговли подключён к экономике игрока."
        )

    if key == "shop":
        return (
            "🛒 МАГАЗИН\n\n"
            f"🪙 Кредиты: {player.credits}\n"
            f"💎 Кристаллы: {player.crystals}\n\n"
            "Магазин подключён как отдельный раздел экономики."
        )

    if key == "systems":
        return (
            "🌌 СИСТЕМЫ STARCORE\n\n"
            "Единый центр игровых систем:\n"
            "• прогресс и экономика\n"
            "• исследование и события\n"
            "• PvE/PvP\n"
            "• социальные механики\n"
            "• гильдии и рейтинги\n"
            "• уведомления и служебные функции"
        )

    return "Раздел не найден. Используйте главное меню."


async def sections(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return
    with SessionLocal() as session:
        get_or_create_player(session, user.id, user.username)
    await message.reply_text(
        "🧩 ВСЕ РАЗДЕЛЫ STARCORE\n\nВыберите нужную систему:",
        reply_markup=sections_keyboard(),
    )


async def section_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.effective_user
    if query is None or user is None:
        return
    await query.answer()
    action = query.data or ""

    if action == "section:all":
        await sections(update, context)
        return

    if action == "section:menu":
        from handlers.menu import main_menu_keyboard
        if query.message:
            await query.message.reply_text("🎮 Главное меню STARCORE", reply_markup=main_menu_keyboard())
        return

    if action == "section:systems":
        from handlers.hub import hub
        await hub(update, context)
        return

    key = action.removeprefix("section:")
    if key not in SECTION_LABELS:
        if query.message:
            await query.message.reply_text("⚠️ Раздел временно недоступен.")
        return

    with SessionLocal() as session:
        player = get_or_create_player(session, user.id, user.username)
        profile = get_or_create_profile(session, player.id)
        text = _section_text(session, player, profile, key)
    if query.message:
        await query.message.reply_text(text, reply_markup=sections_keyboard())
