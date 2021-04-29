from logging import getLogger

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

import commands.help as help_command
import commands.onereport as onereport_command

logger = getLogger()


class HamfakedetBot:
    updater: Updater

    def __init__(self, api_key: str):
        self.updater = Updater(api_key, use_context=True)
        self.api_key = api_key

        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", HamfakedetBot.__handle_start))

        dispatcher.add_handler(onereport_command.get_one_report_handler())

        dispatcher.add_handler(CommandHandler("help", help_command.handler))

        dispatcher.add_handler(CallbackQueryHandler(help_command.callback_handler))
        dispatcher.add_handler(CommandHandler("onereport", help_command.callback_handler))

        dispatcher.add_handler(MessageHandler(Filters.text, HamfakedetBot.__handle_message))
        dispatcher.add_error_handler(HamfakedetBot.__error)

    def start(self, url: str = "", port: int = 8443):
        if self.updater:
            if url:
                self.updater.start_webhook(
                    listen="0.0.0.0",
                    port=port,
                    url_path=self.api_key,
                    webhook_url=f'{url}{self.api_key}'
                )
            else:
                self.updater.start_polling()

            self.updater.idle()

    @staticmethod
    def __handle_start(update: Update, _: CallbackContext):
        update.message.reply_text('המפקדת כאן בשבילך! D:')

    @staticmethod
    def __handle_message(update: Update, _: CallbackContext):
        update.message.reply_text("לא מכירה את זה \U0001F625")

    @staticmethod
    def __error(update: Update, context: CallbackContext):
        logger.error(f"Update {update} caused error {context.error}")
