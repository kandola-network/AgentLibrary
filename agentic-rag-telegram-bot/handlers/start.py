from telegram import Update
from telegram.ext import ContextTypes
from utils.conversation_manager import conversation_manager

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    conversation_manager.clear_conversations(update.effective_chat.id)
    welcome_message = (
        "\nWelcome! I can help you with queries and agent-related tasks.\n\n"
        "**RAG Query**\n"
        "`/query`\n\n"
        "**Agent Query**\n"
        "`/agent`\n"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")
