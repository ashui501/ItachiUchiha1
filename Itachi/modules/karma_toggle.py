import Itachi.modules.mongo.karma_mongo as ksql
import html
from telegram import ParseMode
from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler)
from telegram.utils.helpers import mention_html
from Itachi import  dispatcher

bot_name = f"{dispatcher.bot.first_name}"


def karma_status(update: Update, context: CallbackContext):
    query= update.callback_query
    bot = context.bot
    user = update.effective_user
    if query.data == "add_karma":
        chat = update.effective_chat
        is_chatbot = ksql.is_karma(chat.id)
        if not is_chatbot:
            is_chatbot = ksql.set_karma(chat.id)
            update.effective_message.edit_text(
                f"{bot_name} Karma System Enabled by {mention_html(user.id, user.first_name)}.",
                parse_mode=ParseMode.HTML,
            )
            return
        elif is_chatbot:
            return update.effective_message.edit_text(
                f"{bot_name} Karma System Already Enabled.",
                parse_mode=ParseMode.HTML,
            )
        else:
            return update.effective_message.edit_text(
                "Error!",
                parse_mode=ParseMode.HTML,
            )
    elif query.data == "rem_karma":
        chat = update.effective_chat
        is_chatbot = ksql.is_karma(chat.id)
        if is_chatbot:
            is_chatbot = ksql.rem_karma(chat.id)
            update.effective_message.edit_text(
                f"{bot_name} Karma System disabled by {mention_html(user.id, user.first_name)}.",
                parse_mode=ParseMode.HTML,
            )
            return 
        elif not is_chatbot:
            return update.effective_message.edit_text(
                f"{bot_name} Karma System Already Disabled.",
                parse_mode=ParseMode.HTML,
            )
        else:
            return update.effective_message.edit_text(
                "Error!",
                parse_mode=ParseMode.HTML,
            )


def karma_toggle(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "Choose an option"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Enable",
            callback_data=r"add_karma")],
       [
        InlineKeyboardButton(
            text="Disable",
            callback_data=r"rem_karma")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )

KARMA_STATUS_HANDLER = CommandHandler("karma", karma_toggle, run_async = True)
ADD_KARMA_HANDLER = CallbackQueryHandler(karma_status, pattern=r"add_karma", run_async = True)
RM_KARMA_HANDLER = CallbackQueryHandler(karma_status, pattern=r"rem_karma", run_async = True)

dispatcher.add_handler(ADD_KARMA_HANDLER)
dispatcher.add_handler(KARMA_STATUS_HANDLER)
dispatcher.add_handler(RM_KARMA_HANDLER)

__handlers__ = [
    ADD_KARMA_HANDLER,
    KARMA_STATUS_HANDLER,
    RM_KARMA_HANDLER,
]