import time 
import asyncio
from random import choice
from Itachi import app,get_readable_time
from pyrogram import filters, enums , Client
from Itachi.modules.pyro.permissions import *
from pyrogram.errors import FloodWait 

SPAM_CHATS = []
emoji_unicode_list = [
"\U0001F600", "\U0001F603", "\U0001F604", "\U0001F601", "\U0001F606",
"\U0001F605", "\U0001F923", "\U0001F602", "\U0001F642", "\U0001F643",
"\U0001FAE0", "\U0001F609", "\U0001F60A", "\U0001F607", "\U0001F970",
"\U0001F60D", "\U0001F929", "\U0001F618", "\U0001F617",
"\U0001F61A", "\U0001F619", "\U0001F972", "\U0001F60B", "\U0001F61B",
"\U0001F61C", "\U0001F92A"
]

@Client.on_message(filters.command(["tagall", "all"]) | filters.command("@all", "") & filters.group)
async def tag_all_users(_,message): 
    replied = message.reply_to_message  
    group = await is_group(message.chat.type)
    if not group:
    	return await message.reply_text("**This Command Was Made For Group Not Private.**")
    admin_user = await is_admin(message.chat.id , message.from_user.id)
    if not admin_user:
    	return await message.reply_text("**You Aren't An Admin.**")
    if len(message.command) < 2 and not replied:
        await message.reply_text("**Reply To Message.**") 
        return                  
    if replied:
        SPAM_CHATS.append(message.chat.id)
        start = time.time()        
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id): 
            if message.chat.id not in SPAM_CHATS:
                break       
            usernum += 1
            alpha = choice(emoji_unicode_list)
            usertxt += f"[{alpha}](tg://user?id={m.user.id})"
            if usernum == 5:
                await replied.reply_text(usertxt)
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        end = get_readable_time((time.time() - start))
        await message.reply_text(f"**Mention Completed In** `{end}`")
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        text = message.text.split(None, 1)[1]
        
        SPAM_CHATS.append(message.chat.id)
        start = time.time()
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):       
            if message.chat.id not in SPAM_CHATS:
                break 
            usernum += 1
            alpha = choice(emoji_unicode_list)
            usertxt += f"[{alpha}](tg://user?id={m.user.id})"
            if usernum == 5:
                await app.send_message(message.chat.id,f'{text}\n{usertxt}')
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""            
        end = get_readable_time((time.time() - start))
        await message.reply_text(f"**Mention Completed In** `{end}`")                
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass        
           


@Client.on_message(filters.command("cancel") & filters.group)
async def cancelcmd(_, message):
	group = await is_group(message.chat.type)
    if not group:
    	return await message.reply_text("**This Command Was Made For Group Not Private.**")
    admin_user = await is_admin(message.chat.id , message.from_user.id)
    if not admin_user:
    	return await message.reply_text("**You Aren't An Admin.**")
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try :
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass   
        return await message.reply_text("**Mention Cancelled.**")     
                                     
    else :
        await message.reply_text("**Mention Not Started.**")  
        return       
    
__help__ = """
**Tag Everyone In Chats.**

**Command**

♠ `/tagall` : mention everyone by tagging them.
♠ `/cancel` : cancel current mention process.
"""
__mod_name__ = "Tag-All"
    
