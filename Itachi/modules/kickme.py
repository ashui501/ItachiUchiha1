import html
from telegram import (
    ParseMode,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, CommandHandler, CallbackQueryHandler
from telegram.utils.helpers import mention_html
from typing import Optional
from Itachi import dispatcher

BAN_GIF = "CgACAgUAAxkBAAK0XGLeQb3hs3yWorkBjUMFGMWENA8RAALZBAACT_vxVu249YEwNBU9KQQ"
KICK_GIF = "CgACAgUAAxkBAAK0X2LeQev25-iVt1uCqZ2GMRpe-tnGAALbBAACT_vxVjmenxs25dq2KQQ"


def punchme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text(
            "punches you out of the group!!",
        )
    else:
        update.effective_message.reply_text("Huh? I can't :/")


def banme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    res = update.effective_chat.ban_member(user_id)
    if res:
        update.effective_message.reply_text("You're not worthy to be in my friend group. Goodbye!")
        return (
            "<b>{}:</b>"
            "\n#BANME"
            "\n<b>User:</b> {}"
            "\n<b>ID:</b> <code>{}</code>".format(
                html.escape(chat.title),
                mention_html(user.id, user.first_name),
                user_id,
            )
        )

    else:
        update.effective_message.reply_text("Huh? I can't :/")







KICKME_HANDLER = DisableAbleCommandHandler(["kickme", "punchme"], punchme, filters=Filters.chat_type.groups, run_async=True)
BANME_HANDLER = CommandHandler("banme", banme, run_async=True, filters=Filters.chat_type.groups)


dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(BANME_HANDLER)