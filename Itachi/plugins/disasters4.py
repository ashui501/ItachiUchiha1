from Itachi import app
from Itachi.config import SUDO_USERS,DEV_USERS,SUPER_USERS as SUPREME_USERS , OWNER_ID
from pyrogram import filters ,Client
from Itachi.modules.pyro.extracting_id import extract_user_id
from Itachi.modules.mongo.sudo_db import *
from Itachi.modules.pyro.extracting_id import extract_user_id

@Client.on_message(filters.command("akatsukis") & filters.user(SUPREME_USERS))
async def _devlist(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return 
    msg = "**♠ Akatsuki Users ♠\n**"
    for m in set(DEV_USERS):
        try:
            mention = (await _.get_users(m)).mention
            msg += f"• {mention}\n"
        except Exception as e:
            print(e)
    return await message.reply_text(msg)
