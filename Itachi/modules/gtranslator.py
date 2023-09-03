from gpytranslate import Translator
from telegram.ext import CallbackContext , CommandHandler
from telegram import (
    Message,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from Itachi import dispatcher, app as pbot
from pyrogram import filters, enums



__help__="""
**Lang Translator**

**Commands**

♠ `/tl` (or /tr): as a reply to a message, translates it to English.
♠ `/langs`: get a list of supported languages for translation.

"""
__mod_name__ = "Translator 🈵"


trans = Translator()


@pbot.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Reply to a message to translate it!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>Translated from {source} to {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )

    await message.reply_text(reply, parse_mode= enums.ParseMode.HTML)


def languages(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(
        "Click on the button below to see the list of supported language codes.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Language codes",
                        url="https://telegra.ph/Lang-Codes-03-19-3",
                    ),
                ],
            ],
            disable_web_page_preview=True,
        ),
    )


LANG_HANDLER = CommandHandler("langs", languages, run_async=True)

dispatcher.add_handler(LANG_HANDLER)
