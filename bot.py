from telegram import ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from config import settings
from database.database import init_db
from handlers.menu import hide_menu, menu
from handlers.profile import profile
from handlers.start import start


async def profile_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await profile(update, context)


async def help_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is not None:
        await update.message.reply_text(
            "ℹ️ STARCORE\n\n"
            "/start — запуск игры\n"
            "/menu — открыть главное меню\n"
            "/profile — профиль игрока"
        )


async def play_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is not None:
        await update.message.reply_text("🎮 Игровой раздел готовится. Используйте /menu для навигации.")


async def stats_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is not None:
        await update.message.reply_text("📊 Статистика будет доступна в соответствующей стадии.")


async def notifications_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is not None:
        await update.message.reply_text("🔔 Уведомления настроены через главное меню.")


def build_application() -> Application:
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is not configured")

    application = Application.builder().token(settings.bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(MessageHandler(filters.Regex(r"^🧬 Профиль$"), profile_button))
    application.add_handler(MessageHandler(filters.Regex(r"^🎮 Играть$"), play_button))
    application.add_handler(MessageHandler(filters.Regex(r"^📊 Статистика$"), stats_button))
    application.add_handler(MessageHandler(filters.Regex(r"^🔔 Уведомления$"), notifications_button))
    application.add_handler(MessageHandler(filters.Regex(r"^ℹ️ Помощь$"), help_button))
    application.add_handler(MessageHandler(filters.Regex(r"^❌ Скрыть меню$"), hide_menu))
    return application


def main() -> None:
    init_db()
    application = build_application()
    application.run_polling()


if __name__ == "__main__":
    main()
