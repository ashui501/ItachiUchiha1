import asyncio
import random
from sys import version_info
from pyrogram import __version__ as pver
from pyrogram import filters , Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Itachi import BOT_NAME, BOT_USERNAME, app
from Itachi.config import SUPPORT_CHAT, UPDATES_CHANNEL, OWNER_ID
#from Itachi.__main__ import ITACHI_PIC
from Itachi.modules.pyro.decorators import control_user, command

ITACHI_PIC = ["https://telegra.ph/file/f546e6681709b03255f00.jpg", "https://telegra.ph/file/fa1aab224fb2cbc08f47b.jpg", "https://telegra.ph/file/8b78e64eda3f0af73e186.jpg", "https://telegra.ph/file/1355fde2a2c876810ad02.jpg", "https://telegra.ph/file/607c2911f1dc48d40a4e9.jpg", "https://telegra.ph/file/14043c792ee8e71c4eeb6.jpg"]

__help__ = """
**Here is The Help For Admins**

**Commands**

♠   `/alive` - check the bot is alive or not.

"""
__mod_name__ = "Alive 👾"

ALIVE_TEXT = """**Hey I Am {}
 ━━━━━━━━━━━━━━━━━━━
 » My Master : {}
 » ★ Artificial Robot To Manage Groups
 » ★ Pyrogram : {}
 » Thanks For Adding Me Here 
 ━━━━━━━━━━━━━━━━━━━**"""

btn = [
    [
        InlineKeyboardButton(text="Updates 💻", url=f"https://t.me/{UPDATES_CHANNEL}"),
        InlineKeyboardButton(text="Support 🏥", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="🖤 System Stats 🖤",
            callback_data="Friday_st",
        ),
    ],
    [
        InlineKeyboardButton(
            text="☯️ Add Me To Your Group ☯️",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

@Client.on_message(filters.command("alive"))
@control_user()
async def restart(_, message):
    mention = (await _.get_users(int(OWNER_ID))).mention
    
    accha = await message.reply("⚡")
    await asyncio.sleep(1)
    await accha.edit("**Awakening...**")
    await accha.delete()
    await asyncio.sleep(0.1)
    await message.reply_photo(
        random.choice(ITACHI_PIC),
        caption=ALIVE_TEXT.format(BOT_NAME, mention, pver),
        reply_markup=InlineKeyboardMarkup(btn),
    )
