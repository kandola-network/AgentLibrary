from warnings import filterwarnings
from telegram.ext import Application, CommandHandler
from handlers.start import start
from handlers.query import query_conv_handler
from handlers.agent import agent_conv_handler
from utils.constant import TELEGRAM_TOKEN
from telegram.warnings import PTBUserWarning

filterwarnings("ignore", category=PTBUserWarning)
def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(query_conv_handler)
    application.add_handler(agent_conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
