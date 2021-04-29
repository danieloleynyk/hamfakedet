from datetime import datetime
from logging import getLogger

import pytz
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, JobQueue
from telegram import Update

import responses

logger = getLogger()

TIME_FORMAT = "%H:%M"


class Bot:
    updater: Updater

    def __init__(self, api_key: str):
        self.updater = Updater(api_key, use_context=True)
        self.api_key = api_key

        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", Bot.__start_command))
        dispatcher.add_handler(CommandHandler("onereport", Bot.__one_report_handler))

        dispatcher.add_handler(MessageHandler(Filters.text, Bot.__handle_message))
        dispatcher.add_error_handler(Bot.__error)

    def start(self, url: str = "", port: int = 8443):
        if self.updater:
            if url:
                self.updater.start_webhook(
                    listen="0.0.0.0",
                    port=port,
                    url_path=self.api_key,
                    webhook_url=f'{url}:{port}/{self.api_key}'
                )
            else:
                self.updater.start_polling()
                self.updater.idle()

    @staticmethod
    def __start_command(update: Update, context: CallbackContext):
        update.message.reply_text('המפקדת כאן בשבילך! D:')

    @staticmethod
    def __handle_message(update: Update, context: CallbackContext):
        text = str(update.message.text).lower()
        update.message.reply_text(text)

    @staticmethod
    def __one_report_alarm(context: CallbackContext):
        job = context.job
        context.bot.send_message(str(job.context), text=responses.one_report_notifier())

    @staticmethod
    def __one_report_handler(update: Update, context: CallbackContext):
        """Add a job to the queue."""
        try:
            chat_id = update.message.chat_id

            target_time = datetime.strptime(str(context.args[0]), TIME_FORMAT).time() \
                .replace(tzinfo=pytz.timezone('Asia/Jerusalem'))

            message = f'הפעם לא נכשח למלא דוח1 ב {target_time.strftime("%H:%M")} \U0001F910'

            job_removed = Bot.__remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_daily(Bot.__one_report_alarm, context=chat_id, days=(0, 1, 2, 3, 6),
                                        time=target_time, name=str(chat_id))

            if job_removed:
                message += ' (ההתראה הקודמת נמחקה)'

            update.message.reply_text(message)
        except IndexError:
            update.message.reply_text('מתי להזכיר?? (onereport 08:30)')

    @staticmethod
    def __remove_job_if_exists(name: str, context: CallbackContext) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            logger.info("removed previous job")
            job.schedule_removal()
        return True

    @staticmethod
    def __error(update: Update, context: CallbackContext):
        logger.error(f"Update {update} caused error {context.error}")
