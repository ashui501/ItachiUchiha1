from Itachi import app
from Itachi.config import SUDO_USERS,DEV_USERS,SUPER_USERS as SUPREME_USERS , OWNER_ID
from pyrogram import filters ,Client
from Itachi.modules.pyro.extracting_id import extract_user_id
from Itachi.modules.mongo.sudo_db import *
from Itachi.modules.pyro.extracting_id import extract_user_id



@Client.on_message(filters.command("addkage") & filters.user(DEV_USERS))
async def _addsudo(_, message):
    
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text("**Specify An User.**")

    sudo_users = await get_sudo_list()
    if user_id in sudo_users :
        return await message.reply_text("**User Already In Kage.**") 
    if  user_id in DEV_USERS:
        return await message.reply_text("**This Is An Kage User.**") 
    await add_sudo(user_id)
    if not user_id in SUDO_USERS:
        SUDO_USERS.append(user_id)
        SUPREME_USERS.append(user_id)
    return await message.reply_text("**Added In Kage Users.**")

@Client.on_message(filters.command("rmkage") & filters.user(DEV_USERS))
async def _rmsudo(_, message):
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text("**Specify An User.**")
    sudo_users = await get_sudo_list()
    if user_id not in sudo_users :
        return await message.reply_text("**This User Isn't Kage User.**")  
    await del_sudo(user_id)
    if user_id in SUDO_USERS:
        SUDO_USERS.remove(user_id)
        SUPREME_USERS.remove(user_id)
    return await message.reply_text("**Removed From Kage Users.**")  



@Client.on_message(filters.command("kagelist"))
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

@Client.on_message(filters.command("akatsukilist"))
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
 


