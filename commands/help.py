from telegram.ext import CallbackContext
from telegram import Update


HELP_BUTTON_CALLBACK_DATA = "help command"


def handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, "help help help")


def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text(query.data)
    query.answer()
