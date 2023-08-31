from Itachi import app , BOT_ID
from Itachi.config import SUPER_USERS as CHAD
from pyrogram import filters,enums,Client
from Itachi.modules.pyro.permissions import *
from Itachi.modules.mongo.approve_db import approved_users,isApproved
from Itachi.modules.mongo.blacklistSticker_db import *
blacklist_sticker_watcher = 33


@Client.on_message(filters.command("addblsticker"))
async def _addstick(_, message):
    chat_id = message.chat.id
    group = await is_group(message.chat.type)
    if not group:
    	return await message.reply_text("**This Command Was Made For Group Not Private.**")
    admin_user = await is_admin(message.chat.id , message.from_user.id)
    if not admin_user:
    	return await message.reply_text("**You Aren't An Admin.**")
    delete = await can_delete(message.chat.id , message.from_user.id)
    if not delete:
    	return await message.reply_text("**You don't have permission to delete messages.**")
    delete_bot = await can_delete(message.chat.id , BOT_ID)
    if not delete_bot:
    	return await message.reply_text("**I don't have permission to delete messages.**")
    replied = message.reply_to_message
    if not replied :
        return await message.reply_text("**Reply to Sticker.**")
    if replied and replied.sticker:
        set_name = replied.sticker.set_name                    
    else:
        return await message.reply_text("**Reply to Sticker.**")
    check = await isBlSticker(chat_id,set_name)
    if check :
        return await message.reply_text("**This Sticker Is Already Blacklisted.**")
    await addBlSticker(chat_id,set_name)
    return await message.reply_text("**Added In Blacklist.**")  
        
    
@Client.on_message(filters.command("unblsticker"))
async def _unaddstick(_, message):
    chat_id = message.chat.id
    group = await is_group(message.chat.type)
    if not group:
    	return await message.reply_text("**This Command Was Made For Group Not Private.**")
    admin_user = await is_admin(message.chat.id , message.from_user.id)
    if not admin_user:
    	return await message.reply_text("**You Aren't An Admin.**")
    delete = await can_delete(message.chat.id , message.from_user.id)
    if not delete:
    	return await message.reply_text("**You don't have permission to delete messages.**")
    delete_bot = await can_delete(message.chat.id , BOT_ID)
    if not delete_bot:
    	return await message.reply_text("**I don't have permission to delete messages.**")
    replied = message.reply_to_message
    if not replied :
        return await message.reply_text("**Reply to Sticker.**")
    if replied and replied.sticker:
        set_name = replied.sticker.set_name                    
    else:
        return await message.reply_text("**Reply to Sticker.**")
    check = await isBlSticker(chat_id,set_name)
    if check:
        await unBlSticker(chat_id,set_name)
        return await message.reply_text("**Removed Sticker From Blacklist.**")
    return await message.reply_text("**This Sticker Isn't Blacklisted.**")
    
@Client.on_message(filters.sticker & filters.group, group=blacklist_sticker_watcher)
async def _delstick(_, message):
    chat_id = message.chat.id
    user = message.from_user
    list1 = await blacklisted_stickers(chat_id) 
    if not list1:
        return 
    xx = await _.get_chat_member(chat_id,user.id)        
    if (xx.privileges) or (user.id in SUPREME_USERS) or (await isApproved(chat_id,user.id)):
        return       
    set_name = message.sticker.set_name 
    try:      
        if set_name in list1:
            return await message.delete()
    except:
        pass
        
        
   

    
