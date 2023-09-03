import requests
from Itachi import dispatcher
from telegram.ext import CommandHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

n = "\n"
w = " "

bold = lambda x: f"**{x}:** "
bold_ul = lambda x: f"**--{x}:**-- "

mono = lambda x: f"`{x}`{n}"


def section(
        title: str,
        body: dict,
        indent: int = 2,
        underline: bool = False,
) -> str:
    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        text += (
                indent * w
                + bold(key)
                + ((value[0] + n) if isinstance(value, list) else mono(value))
        )
    return text


def crypto(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args
    if len(args) == 0:
        return message.reply_text("/crypto [currency]")

    currency = message.text.split(None, 1)[1].lower()

    buttons = [
        [
            InlineKeyboardButton(text = "Available Currencies", url ="https://plotcryptoprice.herokuapp.com"),
        ],
    ]

    try:
        url = f'https://x.wazirx.com/wazirx-falcon/api/v2.0/crypto_rates'
        result = requests.get(url).json()
    except Exception:
        return message.reply_text("[ERROR]: Something went wrong.")

    if currency not in result:
        return update.effective_message.reply_text(
            "[ERROR]: INVALID CURRENCY",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    body = {i.upper(): j for i, j in result.get(currency).items()}

    text = section(
        "Current Crypto Rates For " + currency.upper(),
        body,
    )
    update.effective_message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)

CRYPTO_HANDLER = CommandHandler("crypto", crypto, run_async=True)

dispatcher.add_handler(CRYPTO_HANDLER)

__handlers__ = [
    CRYPTO_HANDLER
]


__mod_name__ = "Crypto "
__help__="""
**Crypto values**

**Commands**

 `/crypto` [currency] :Get Real Time value from currency given.

"""