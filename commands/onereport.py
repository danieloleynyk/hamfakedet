from datetime import datetime

import pytz
import logging
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove

import responses
from commands.utils import remove_job_if_exists


ONEREPORT_BUTTON_CALLBACK_DATA = "onereport command"
TIME_FORMAT = "%H:%M"


CHOOSE_TIME, SCHEDULE = range(2)


logger = logging.getLogger()


def get_one_report_handler() -> ConversationHandler:
    time_options = ['08:00', '08:30', '09:00', 'אחר']

    def choose_time_from_options(update: Update, _: CallbackContext) -> int:
        reply_keyboard = [time_options]

        update.message.reply_text(
            'אזכיר לך בשעה:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return SCHEDULE

    def choose_other_time(update: Update, _: CallbackContext) -> int:
        update.message.reply_text(
            'באיזה שעה? (לדוגמה 08:45)',
            reply_markup=ReplyKeyboardRemove(),
        )

        return SCHEDULE

    def schedule(update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id

        target_time = datetime.strptime(update.message.text, TIME_FORMAT).time() \
            .replace(tzinfo=pytz.timezone('Asia/Jerusalem'))

        message = f'הפעם לא נשכח למלא דוח1 ב {target_time.strftime("%H:%M")} \U0001F910'

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_daily(__one_report_alarm, context=chat_id, days=(0, 1, 2, 3, 6),
                                    time=target_time, name=str(chat_id))

        if job_removed:
            message += ' (ההתראה הקודמת נמחקה)'

        update.message.reply_text(message)

        return ConversationHandler.END

    def cancel(update: Update, _: CallbackContext) -> int:
        update.message.reply_text(
            'מנסה לעשות לי בלאגן? לא רוצה לא צריך...', reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    return ConversationHandler(
        entry_points=[CommandHandler('onereport', choose_time_from_options)],
        states={
            SCHEDULE: [
                MessageHandler(Filters.regex(f'^({time_options[-1]})$'), choose_other_time),
                MessageHandler(Filters.regex('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'), schedule),
            ]
        },
        fallbacks=[MessageHandler(Filters.text, cancel)],
    )


def __one_report_alarm(context: CallbackContext):
    job = context.job
    context.bot.send_message(str(job.context), text=responses.one_report_notifier())
