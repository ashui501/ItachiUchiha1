from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from Itachi import BOT_NAME,BOT_USERNAME,app
from Itachi.config import OWNER_ID, SUPPORT_CHAT,UPDATES_CHANNEL


PM_START_TEXT = """
────「 {} 」────
Hola! {} ,
I am an Anime themed advance group management bot based Itachi Uchiha ✨
➖➖➖➖➖➖➖➖➖➖➖➖➖
‣ Uptime: {}
‣ Python: {}
‣ Pyrogram: {}
➖➖➖➖➖➖➖➖➖➖➖➖➖
‣ Keep Your Group Secure From Spammers by Adding me ✨
"""

SUPPORT_SEND_MSG = """
**Itachi Uchiha !**
**Python Version:** `{}`
**Pyrogram Version:** `{}`
**UpTime:** `{}`
"""

LOG_MSG = "Itachi Uchiha Started ✨"

HELP_STRINGS = f"""**
Click on below buttons to access commands of {BOT_NAME}.**
"""

START_BUTTONS = [
    [
        InlineKeyboardButton(text="Help 🚨", callback_data="help_back"),
        InlineKeyboardButton(text="Support 🆘", url=f"t.me/{SUPPORT_CHAT}")
    ], 
    [
        InlineKeyboardButton(text="Music 🎶", callback_data="music_p"),
        InlineKeyboardButton(text="Ai 🤖", callback_data="ai_help")
    ], 
    [
        InlineKeyboardButton(
            text="☯️ Add Itachi To Group ☯️",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],     
]
GRP_START = [
    [
        InlineKeyboardButton(text="Updates", url=f"t.me/{UPDATES_CHANNEL}"),
        InlineKeyboardButton(text="Support", url=f"t.me/{SUPPORT_CHAT}")
    ], 
    [
       InlineKeyboardButton("System Stats",callback_data="Friday_st")
    ],
]
BACK_BTN = [[InlineKeyboardButton("🔙",callback_data="friday_back")]]
MUSIC_BTN = [
    [
        InlineKeyboardButton(text="Admin Commands 🐥", callback_data="admin_music"),
        InlineKeyboardButton(text="Play Commands 🍼", callback_data="play_music")
    ], 
    [
       InlineKeyboardButton("Back 🔙",callback_data="friday_back")
    ],
]
MUSIC_BACK =  [[InlineKeyboardButton("🔙",callback_data="m_back")]]
