from Itachi import app,BOT_ID,BOT_NAME
from Itachi.config import SUPPORT_CHAT
from pyrogram import filters , Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from Itachi.modules.pyro.permissions import *
from .mongo.actions_db import *
from .pyro.decorators import control_user,command

__help__ = """
**Keep Track Of Chat Actions**

**Commands**

♠ `/addaction` - start receiving chat actions.
♠ `/rmaction` - stop receiving chat actions.

"""
__mod_name__ = "Actions 🐥"


@Client.on_message(filters.command(["addaction","rmaction"]))
@control_user()
async def _mm(_, message):
    chat_id = message.chat.id
    admin_user = await is_admin(message.chat.id , message.from_user.id)
    if not admin_user:
    	return await message.reply_text("**You Aren't An Admin.**")
    check = await isEnbale(chat_id)
    if message.command[0] == "addaction":
        if check:
            return await message.reply_text("**Chat Actions Is Already Enabled In This Group.**")
        await add_action(chat_id)
        return await message.reply_text("**Enabled Chat Actions.**")
    if message.command[0] == "rmaction":
        if not check:
            return await message.reply_text("**Chat Actions Is Already Disabled In This Group.**")
        await rm_action(chat_id)
        return await message.reply_text("**Disabled Chat Actions.**")
    

btn = InlineKeyboardMarkup([[InlineKeyboardButton("Close ❌",callback_data="admin_close")]])
        
@Client.on_chat_member_updated()
async def _cmu(_,cmu):
    chat_id = cmu.chat.id
    old_user = cmu.old_chat_member
    new_user = cmu.new_chat_member
    check = await isEnbale(chat_id)
    if not check:
        return
    if cmu.from_user.id == BOT_ID:
        return 
    try:
        if old_user.status == ChatMemberStatus.ADMINISTRATOR:
            if new_user.status == ChatMemberStatus.MEMBER:
                await _.send_message(chat_id,f"**{BOT_NAME}\n• Demoted An Admin\n• Demoted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)
        
        if old_user.status != ChatMemberStatus.ADMINISTRATOR and new_user.status == ChatMemberStatus.ADMINISTRATOR:  
            if not new_user.custom_title:      
                await _.send_message(chat_id,f"**{BOT_NAME}\n• Promoted An User\n• Promoted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)         
            if new_user.custom_title:
                await _.send_message(chat_id,f"**{BOT_NAME}\n• Promoted An User\n• Promoted: {new_user.user.mention}\n• Title: {new_user.custom_title}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)  
          
        if old_user.status != ChatMemberStatus.RESTRICTED and new_user.status == ChatMemberStatus.RESTRICTED:
            await _.send_message(chat_id,f"**{BOT_NAME}\n• Muted An User\n• Muted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)
        if old_user.status == ChatMemberStatus.RESTRICTED and new_user.status != ChatMemberStatus.RESTRICTED:
            await _.send_message(chat_id,f"**{BOT_NAME}\n• UnMuted An User\n• UnMuted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)

        if old_user.status != ChatMemberStatus.BANNED and new_user.status == ChatMemberStatus.BANNED:
            await _.send_message(chat_id,f"**{BOT_NAME}\n• Banned An User\n• Banned: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)
    except Exception as e:
        pass

