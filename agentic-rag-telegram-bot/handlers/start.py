from telegram import Update
from telegram.ext import ContextTypes
from utils.conversation_manager import conversation_manager

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    conversation_manager.clear_conversations(update.effective_chat.id)
    welcome_message = (
        "Welcome! I can help you with queries and agent-related tasks.\n\n"
        "Available commands:\n"
        "/query - Submit a query\n"
        "/agent - Access agent functionality\n"
    )
    await update.message.reply_text(welcome_message)
