from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from utils.api_calls import make_query_call

WAITING_FOR_QUERY = 1
WAITING_FOR_CATEGORY = 2

async def query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['flow'] = 'query'
    keyboard = [
        [InlineKeyboardButton("Health", callback_data='Health')],
        [InlineKeyboardButton("Finance", callback_data='Finance')],
        [InlineKeyboardButton("Journal", callback_data='Journal')],
        [InlineKeyboardButton("Messaging", callback_data='Messaging')],
        [InlineKeyboardButton("Mail", callback_data='Mail')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select the RAG category:", reply_markup=reply_markup)
    return WAITING_FOR_CATEGORY

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['rag_category'] = query.data
    await query.edit_message_text(text=f"Selected category: {query.data}\nPlease enter your query:")
    return WAITING_FOR_QUERY

async def handle_query_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query_text = update.message.text
    rag_category = context.user_data.get('rag_category', 'Health')
    chat_id = update.effective_chat.id
    try:
        await update.message.chat.send_action(action="typing")
        response = await make_query_call(chat_id, query_text, rag_category)
        await update.message.reply_text(f"Query Response:\n```json\n{response}\n```", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error processing your query: {str(e)}")
    return ConversationHandler.END

query_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("query", query)],
    states={
        WAITING_FOR_CATEGORY: [CallbackQueryHandler(handle_category_selection)],
        WAITING_FOR_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query_input)],
    },
    fallbacks=[],
)
