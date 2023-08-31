from pyrogram import filters,enums,Client
from Itachi import app,db , BOT_ID
from Itachi.config import SUPER_USERS as SUPREME_USERS,SUPER_USERS as CHAD
from Itachi.modules.mongo.approve_db import approved_users , isApproved
from Itachi.modules.pyro.permissions import *
from Itachi.modules.mongo.blacklist_db import *
blacklist_watcher = 69

@Client.on_message(filters.command('addblacklist'))
async def _addblacklist(_, message):
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
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("**Usage :** `/addblacklist <text>`")
    word = args[1].lower()
    check = await is_blacklisted(chat_id,word)
    if not check:
        await add_blacklist(chat_id,word)
        return await message.reply_text("**Blacklisted : {}.**".format(word))
    return await message.reply_text("**{} Is Already Blacklisted.**".format(word))

@Client.on_message(filters.command('rmblacklist'))
async def _addblacklist(_, message):
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
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("**Usage :** `/rmblacklist <text>`")
    word = args[1].lower()
    check = await is_blacklisted(chat_id,word)
    print(check)
    if check:
        await rm_blacklist(chat_id,word)
        return await message.reply_text("**{} Removed From Blacklist.**".format(word))
    return await message.reply_text("**{} Isn't Blacklisted.**".format(word))


@Client.on_message(filters.command("blacklists"))
async def _get_blackisted(_, message):
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
    chat_title = message.chat.title
    words = await get_blacklist(chat_id)
    if not words:
        return await message.reply_text(f"**There Is No Blacklisted Word In {chat_title}**")
    msg = f"**Blacklisted Words In {chat_title}**\n"
    for mm in words:
        msg += f"• `{mm}`\n"
    return await message.reply_text(msg)


@Client.on_message(filters.command("unblacklistall") & filters.group)
async def _get_blackisted(_, message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    user = message.from_user
    if user.status != enums.ChatMemberStatus.OWNER and user.id not in SUPREME_USERS:
        return await message.reply_text("**Only Owner Can Use This Command.**")
    words = await get_blacklist(chat_id)
    if not words:
        return await message.reply_text(f"**There Is No Blacklisted Words In {chat_title}**")
    await un_blacklistall(chat_id)
    return await message.reply_text("**UnBlacklisted All Words.**")
       
    

@Client.on_message(filters.group, group=blacklist_watcher)
async def _delstick(_, message):
    chat_id = message.chat.id
    list1 = await get_blacklist(chat_id)
    
    if not list1:
        return 
    user = message.from_user
    xx = await _.get_chat_member(chat_id,message.from_user.id)        
    if (xx.privileges) or (user.id in SUPREME_USERS) or (await isApproved(chat_id,user.id)): 
        return    
    text = message.text or message.caption
    if text:
        word = message.text.split() if message.text else message.caption.split() 
        for _ in word:
            if _.lower() in list1:
                try:
                    await message.delete()
                except:
                    pass 
            
