from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


MENU_BUTTONS = (
    (("🧬 Профиль", "menu:profile"), ("🎮 Играть", "menu:play")),
    (("📊 Статистика", "menu:stats"), ("🔔 Уведомления", "menu:notifications")),
    (("ℹ️ Помощь", "menu:help"), ("❌ Скрыть меню", "menu:hide")),
)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text, callback_data=data) for text, data in row]
            for row in MENU_BUTTONS
        ]
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(
        "🎮 Главное меню STARCORE\n\nВыберите нужный раздел:",
        reply_markup=main_menu_keyboard(),
    )


async def hide_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text("Меню скрыто. Используйте /menu, чтобы открыть его снова.")
