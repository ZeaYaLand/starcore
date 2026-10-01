import logging

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters

from config import settings
from database.database import init_db
from handlers.menu import hide_menu, main_menu_keyboard, menu
from handlers.notifications import notifications, mark_notifications_read
from handlers.profile import profile
from handlers.start import start
from handlers.stats import stats


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("starcore.bot")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled Telegram update error: %r", context.error, exc_info=context.error)


async def profile_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await profile(update, context)


async def help_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is not None:
        await message.reply_text(
            "ℹ️ STARCORE\n\n"
            "/start — запуск игры\n"
            "/menu — открыть главное меню\n"
            "/profile — профиль игрока\n"
            "/stats — статистика игрока\n"
            "/notifications — уведомления\n"
            "/notifications_read — отметить уведомления прочитанными"
        )


async def play_button(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is not None:
        await message.reply_text("🎮 Игровой раздел готовится. Используйте /menu для навигации.")


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return

    await query.answer()
    action = query.data

    if action == "menu:profile":
        await profile(update, context)
    elif action == "menu:play":
        await play_button(update, context)
    elif action == "menu:stats":
        await stats(update, context)
    elif action == "menu:notifications":
        await notifications(update, context)
    elif action == "menu:help":
        await help_button(update, context)
    elif action == "menu:hide":
        if query.message is not None:
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text("Меню скрыто. Используйте /menu, чтобы открыть его снова.")


def build_application() -> Application:
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is not configured")

    application = Application.builder().token(settings.bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("notifications", notifications))
    application.add_handler(CommandHandler("notifications_read", mark_notifications_read))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern=r"^menu:"))
    application.add_handler(MessageHandler(filters.Regex(r"^🧬 Профиль$"), profile_button))
    application.add_handler(MessageHandler(filters.Regex(r"^🎮 Играть$"), play_button))
    application.add_handler(MessageHandler(filters.Regex(r"^📊 Статистика$"), stats))
    application.add_handler(MessageHandler(filters.Regex(r"^🔔 Уведомления$"), notifications))
    application.add_handler(MessageHandler(filters.Regex(r"^ℹ️ Помощь$"), help_button))
    application.add_handler(MessageHandler(filters.Regex(r"^❌ Скрыть меню$"), hide_menu))
    application.add_error_handler(error_handler)
    return application


def main() -> None:
    logger.info("STARCORE bot starting")
    init_db()
    logger.info("Database initialized")
    application = build_application()
    logger.info("Telegram application built; starting polling")
    application.run_polling()


if __name__ == "__main__":
    main()
