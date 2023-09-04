import os
import requests
import json
import asyncio
from Itachi import app,BOT_USERNAME,BOT_ID, BOT_NAME,db
from pyrogram import filters,enums, Client
from pyrogram.types import Message , InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery 
from Itachi.modules.pyro.chat_actions import send_action
from Itachi.modules.mongo.chatbot_db import chatbotdb,addchat_bot,rmchat_bot


buttons = InlineKeyboardMarkup([[ InlineKeyboardButton(text="Enable", callback_data="add_chat"),InlineKeyboardButton(text="Disable", callback_data="rm_chat")]])  

@Client.on_message(filters.command("chatbot"))
async def _check_bot(_, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.chat.type != enums.ChatType.PRIVATE:
        xx = await _.get_chat_member(chat_id,user_id)
        if xx.privileges:           
            return await message.reply_text("**Choose An Option.**",reply_markup=buttons)
        else:
            return await message.reply_text("**You need to be admin to use this command.**")
    else:
        return await message.reply_text("**Choose An Option.**",reply_markup=buttons)
    

@Client.on_callback_query(filters.regex("add_chat"))
async def _addchat(app : Client, query : CallbackQuery):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    check_chat = await chatbotdb.find_one({"chat_id" : chat_id})
    if query.message.chat.type != enums.ChatType.PRIVATE:
        
        xx = await app.get_chat_member(chat_id,user_id)
        if xx.privileges:    
            if not check_chat:  
                await addchat_bot(chat_id)           
                return await query.message.edit_caption("**Enabled Chatbot in This Chat!**")      
                
            elif check_chat:
                await query.message.edit_caption("**Chatbot is already enabled in this chat.**")
            
   
        else:
            await client.answer_callback_query(
            query.id,
            text = "You can't do that.",
            show_alert = True)
    else:
        if not check_chat:
            await addchat_bot(user_id)                     
            return await query.message.edit_caption("**Enabled Chatbot in This Chat!**") 
        elif check_chat:
            await query.message.edit_caption("**Chatbot is already enabled in this chat.**")   
             
@Client.on_callback_query(filters.regex("rm_chat"))
async def _rmchat(app : Client, query : CallbackQuery):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    check_chat = await chatbotdb.find_one({"chat_id" : chat_id})
  
    if query.message.chat.type != enums.ChatType.PRIVATE:
        xx = await app.get_chat_member(chat_id,user_id)
        if xx.privileges:    
            if check_chat:  
                await rmchat_bot(chat_id)           
                return await query.message.edit_caption("**Disabled Chatbot in This Chat!**")      
                
            elif not check_chat:
                await query.message.edit_caption("Chatbot is already disabled in this chat.**")
            
   
        else:
            await client.answer_callback_query(
            query.id,
            text = "You can't do that.",
            show_alert = True)
    else:
        if check_chat:
            await rmchat_bot(user_id)                     
            return await query.message.edit_caption("**Disabled Chatbot in This Chat!**") 
        elif not check_chat:
            await query.message.edit_caption("**Chatbot is already disabled in this chat.**")   
                 


async def itachi_message(message : Message):
    reply_message = message.reply_to_message
    if message.text.lower() == "itachi":
        return True
    elif BOT_USERNAME in message.text.upper():
        return True
    elif reply_message:
        if reply_message.from_user.id == BOT_ID:
            return True
    else:
        return False

@Client.on_message(filters.text  & ~filters.bot & ~filters.via_bot,group=9)
async def chatbot(_, message): 
    chat_id = message.chat.id
    check_chat = await chatbotdb.find_one({"chat_id" : chat_id})
    if not check_chat:
        return        
    if message.text and not message.document:
        if not await itachi_message(message):
            return  
        await _.send_chat_action(chat_id, enums.ChatAction.TYPING)      
        url = f"https://api.safone.me/chatbot?query={message.text}&user_id=69&bot_name=itachi%20uchiha&bot_master=alpha"
        results = requests.get(url).json() 
        await asyncio.sleep(0.5)
        to_reply = results["response"]
        if "safone" in to_reply.lower():
            to_reply = to_reply.replace("Safone","⏤͟͞ 𝙉𝘼𝙉𝙊™ 🇮🇳")
            to_reply = to_reply.replace("t.me/asmsafone","t.me/GenXNano")
        await message.reply_text(to_reply)
