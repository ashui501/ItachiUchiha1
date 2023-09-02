from Itachi import app
from Itachi.config import SUDO_USERS,DEV_USERS,SUPER_USERS as SUPREME_USERS , OWNER_ID
from pyrogram import filters ,Client
from Itachi.modules.pyro.extracting_id import extract_user_id
from Itachi.modules.mongo.sudo_db import *
from Itachi.modules.pyro.extracting_id import extract_user_id

@Client.on_message(filters.command("rmkage") & filters.user(DEV_USERS))
async def _rmsudo(_, message):
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text("**Specify An User.**")
    if user_id not in SUDO_USERS:
        return await message.reply_text("**This User Isn't Kage User.**")  
    if user_id in SUDO_USERS:
        SUDO_USERS.remove(user_id)
        SUPREME_USERS.remove(user_id)
    return await message.reply_text("**Removed From Kage Users.**")  

