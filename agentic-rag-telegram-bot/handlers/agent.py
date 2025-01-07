from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from utils.api_calls import make_agent_call
import io

WAITING_FOR_AGENT = 1

async def agent(update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message:
        print("Received update without a message.")
        return ConversationHandler.END  # End the conversation if there's no message
    
    await update.message.reply_text("Please enter your question for the agent:")
    return WAITING_FOR_AGENT

async def handle_agent_input(update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message:
        print("Received update without a message.")
        return ConversationHandler.END
    
    agent_text = update.message.text
    chat_id = update.effective_chat.id
    try:
        await update.message.chat.send_action(action="typing")
        response = await make_agent_call(chat_id, agent_text)

        # Ensure response is a string
        if not isinstance(response, str):
            response = str(response)

        # Handle message length
        if len(response) < 4000:
            await update.message.reply_text(
                f"Agent Response:\n```\n{response}\n```",
                parse_mode='Markdown',
            )
        elif len(response) >= 4096:  # Split if moderately long
            chunk_size = 4000
            for i in range(0, len(response), chunk_size):
                chunk = response[i:i + chunk_size]
                await update.message.reply_text(chunk, parse_mode=None)
        else:
            # Send as a file for very large responses
            file_content = io.StringIO(response)
            file_content.name = "agent_response.txt"
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_content,
                caption="Response is too large to display. Download the file to view the full response."
            )
    except Exception as e:
        print(f"Error: {str(e)}")
        await update.message.reply_text(f"Error processing your agent request: {str(e)}")
    return ConversationHandler.END

agent_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("agent", agent)],
    states={
        WAITING_FOR_AGENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_agent_input)],
    },
    fallbacks=[],
)
