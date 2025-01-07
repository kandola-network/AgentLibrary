from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from utils.api_calls import make_agent_call

WAITING_FOR_AGENT = 1

async def agent(update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your question for the agent:")
    return WAITING_FOR_AGENT

async def handle_agent_input(update, context: ContextTypes.DEFAULT_TYPE) -> int:
    agent_text = update.message.text
    chat_id = update.effective_chat.id
    try:
        await update.message.chat.send_action(action="typing")
        response = await make_agent_call(chat_id, agent_text)
        await update.message.reply_text(f"Agent Response:\n```json\n{response}\n```", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error processing your agent request: {str(e)}")
    return ConversationHandler.END

agent_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("agent", agent)],
    states={
        WAITING_FOR_AGENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_agent_input)],
    },
    fallbacks=[],
)
