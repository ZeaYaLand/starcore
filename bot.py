from telegram.ext import Application, CommandHandler

from config import settings
from database.database import init_db
from handlers.profile import profile
from handlers.start import start


def build_application() -> Application:
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is not configured")

    application = Application.builder().token(settings.bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))
    return application


def main() -> None:
    init_db()
    application = build_application()
    application.run_polling()


if __name__ == "__main__":
    main()
