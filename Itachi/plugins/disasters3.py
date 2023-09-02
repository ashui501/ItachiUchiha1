from Itachi import app
from Itachi.config import SUDO_USERS,DEV_USERS,SUPER_USERS as SUPREME_USERS , OWNER_ID
from pyrogram import filters ,Client
from Itachi.modules.pyro.extracting_id import extract_user_id
from Itachi.modules.mongo.sudo_db import *
from Itachi.modules.pyro.extracting_id import extract_user_id

@Client.on_message(filters.command("kages"))
async def _rmsudo(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return 
    if not SUDO_USERS:
        return await message.reply_text("**There Is No Kage Users.**")
    msg = "**♠ Kage Users ♠\n**"
    for m in set(SUDO_USERS):
        try:
            mention = (await _.get_users(int(m))).mention 
            msg += f"• {mention}\n"
        except Exception as e:
            print(e)
    await message.reply_text(msg)
