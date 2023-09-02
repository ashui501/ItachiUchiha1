import os
import datetime
from Itachi import app, BOT_NAME,LOG,BOT_USERNAME as MENTION_BOT
from pyrogram import filters , Client 
from telegraph import upload_file
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from telegraph import Telegraph




telegraph = Telegraph()
new_user = telegraph.create_account(short_name=BOT_NAME)
auth_url = new_user["auth_url"]

@Client.on_message(filters.command(["tgm","tgt"]))
async def upload_media_text_to_telegraph(app, message):
    replied = message.reply_to_message          
    if message.command[0] == "tgm":        
        if not replied:
            await message.reply_text("**reply to a media.**")
            return 
    
        elif replied.media:
            start = datetime.now()
            text = await message.reply("**fetching.....**")
            media = await replied.download()
            end = datetime.now()
            time = (end - start).seconds
            await text.edit_text(text=f"**uploading.....**", disable_web_page_preview=True)
            try:
                downloaded_file = upload_file(media)
            except Exception as error:
                LOG.print(f"[bold red]{error}")
               # await pgram.send_message(ERROR_LOGS,error)
                await text.edit(text=f"**Error** :- {error}", disable_web_page_preview=True)       
                return 

            try:
                os.remove(media)
            except Exception as error:
                LOG.print(f"[bold red]{error}")
                return   
            
            await text.edit(
        
        text=f"**[Here is your telegraph link](https://graph.org{})**".format(downloaded_file[0]),        
        reply_markup=InlineKeyboardMarkup( [
            [
            InlineKeyboardButton(text="Link", url=f"https://graph.org{downloaded_file[0]}")
            ],
          ]
        )
      )

            
        else:
            await message.reply_text("**Invalid Media.**")
            return 

    if message.command[0] == "tgt":        
        if not replied:
            await message.reply_text("**reply to a text**")
            return 
    
        elif replied.text:
          #  text = await message.reply("ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ....")
            response = telegraph.create_page(title=BOT_NAME,html_content=(replied.text.html).replace("\n", "<br>"),author_name=str(message.from_user.first_name),author_url = f'https://telegram.dog/{message.from_user.username}' if message.from_user.id else None)
            await message.reply_text(
        text=f"**[Here is your telegraph link]({})**".format(https://telegra.ph/{response["path"]}),
        reply_markup=InlineKeyboardMarkup( [
            [
            InlineKeyboardButton(text="Link", url=f"https://telegra.ph/{response['path']}")
            ],
          ]
        )
      )
        else:
            await message.reply_text("**Invalid Format.**")
            return 
                                           
__help__ = """
**Upload media or text in telegraph**

**Commands** :

♠ `/tgm` : upload media to telegraph.
♠ `/tgt` : upload text to telegraph.

"""    
__mod_name__ = "Telegraph 🎀"
