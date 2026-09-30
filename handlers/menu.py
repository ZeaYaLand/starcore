from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes


MENU_BUTTONS = (
    ("🧬 Профиль", "🎮 Играть"),
    ("📊 Статистика", "🔔 Уведомления"),
    ("ℹ️ Помощь", "❌ Скрыть меню"),
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [list(row) for row in MENU_BUTTONS],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите раздел STARCORE",
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "🎮 Главное меню STARCORE\n\nВыберите нужный раздел:",
        reply_markup=main_menu_keyboard(),
    )


async def hide_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "Меню скрыто. Используйте /menu, чтобы открыть его снова."
    )
