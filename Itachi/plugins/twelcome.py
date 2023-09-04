import random 
import os
from Itachi import app
from pyrogram import filters ,enums , Client
from unidecode import unidecode
from Itachi.modules.pyro.status import user_admin,user_can_change_info            
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from Itachi.resources.Data import LOCATION , WEL_PIC
from Itachi.utils.drawing import (
    minimal1,
    minimal2,
    animin1,
    animin2,
    animin3,
    gamin ,
    sun,
    gamin1,
    wholesome,
    meriloli,
    animegirl1,
    animegirl2)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , CallbackQuery 
from Itachi.modules.mongo.twelcome_db import is_welcome_on,del_welcome,set_custom_welcome,get_custom_welcome
welcome_watcher = 69

async def check_temp(chat_id,pfp,name,chat_title,user_id,username,count):
    chat_title = unidecode(chat_title).upper()
    locate = await get_custom_welcome(chat_id)
    if not locate:
        welpic = await minimal1(pfp=pfp,chat=chat_title,id=user_id)
    if locate == LOCATION[1]:
        welpic = await minimal1(pfp=pfp,chat=chat_title,id=user_id)
    if locate == LOCATION[2]:
        welpic = await minimal2(pfp=pfp,chat=chat_title,id=user_id)
    if locate == LOCATION[3]:
        welpic = await animin1(pfp=pfp,name=name,id=user_id,username=username)
    if locate == LOCATION[4]:
        welpic = await animin2(name=name,id=user_id,username=username,chat=chat_title)
    if locate == LOCATION[5]:
        welpic = await animin3(pfp=pfp, name=name,id = user_id,username=username, chat=chat_title)
    if locate == LOCATION[6]:
        welpic = await gamin(pfp=pfp,chat=chat_title,name=name,id=user_id, username=username)
    if locate == LOCATION[7]:
        welpic = await sun(pfp=pfp,chat=chat_title,count=count,id=user_id)
    if locate == LOCATION[8]:
        welpic = await gamin1(pfp=pfp,name=name, username=username,id=user_id)
    if locate == LOCATION[9]:
        welpic = await wholesome(pfp=pfp,chat=chat_title,id=user_id)
    if locate == LOCATION[10]:
        welpic = await meriloli(pfp=pfp,chat=chat_title,id=user_id)  
    if locate == LOCATION[11]:
        welpic = await animegirl1(pfp=pfp,id=user_id)  
    if locate == LOCATION[12]:
        welpic = await animegirl2(pfp=pfp,id=user_id)            
    return welpic 
  

@Client.on_message(filters.new_chat_members & filters.group,group=welcome_watcher)
async def _welmem(_, message):    
    chat_id = message.chat.id   
    bsdk = await is_welcome_on(chat_id)
    if not bsdk:
        return 
    chat_title = message.chat.title 
    count = await _.get_chat_members_count(chat_id) 
    for m in message.new_chat_members:
        name = m.first_name 
        username = m.username
        mention = m.mention 
        user_id = m.id       
        try:
            user_photo = m.photo.big_file_id
            pic = await _.download_media(m.photo.big_file_id,file_name =f"pp{user_id}.png")
        except AttributeError:
            pic = "./Itachi/resources/pics/profilepic.png"
        welpic = await check_temp(chat_id,pic,name,chat_title,user_id,username,count)
        await _.send_photo(chat_id,welpic,caption=f"**Hey {mention} , welcome to {chat_title} !**")
        os.remove(welpic)
        if user_photo:
            os.remove(pic)
    

@Client.on_callback_query(filters.regex(pattern=r"open#(.*)"))
async def _temp(_, query):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    if user_id != int(query.data.split("#")[1]):
        return await _.answer_callback_query(query.id,"Not for you.")
    index = int(query.data.split("#")[2])   
    await query.message.reply_photo(LOCATION[index],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• Preview •",url=WEL_PIC[index])],[InlineKeyboardButton("• Save •", callback_data=f"save#{user_id}#{index}")]]))      
    await query.message.delete() 
            
@Client.on_callback_query(filters.regex(pattern=r"save#(.*)"))
async def _temp(_, query):
    chat_id = query.message.chat.id        
    user_id = query.from_user.id 
    if user_id != int(query.data.split("#")[1]):
        return await _.answer_callback_query(query.id,"Not for you.")
    index = int(query.data.split("#")[2])   
    await query.message.edit_caption("**Template Welcome Successfully Set.**")     
    await set_custom_welcome(chat_id,LOCATION[index]) 

@Client.on_message(filters.command("setwelcome") & filters.group)
@user_admin
@user_can_change_info
async def _well(_, message):
    user_id = message.from_user.id
    index = 1
    return await message.reply_photo(photo=LOCATION[1],caption="**Click on below button to set welcome image.**",
        reply_markup = InlineKeyboardMarkup([
            [ InlineKeyboardButton(
                    text=f"• Open •",
                    callback_data=f"open#{user_id}#{index}",
                ),
                InlineKeyboardButton(
                    text=f"• Next •",
                    callback_data=f"welnxt#{user_id}#{index}",
                )
            ]
        ] ),
        )            
    

@Client.on_callback_query(filters.regex(pattern=r"welnxt#(.*)"))
async def _temp(_, query):
    await query.message.delete()
    chat_id = query.message.chat.id        
    user_id = query.from_user.id 
    index = int(query.data.split("#")[2]) + 1
    print(index)
    if user_id != int(query.data.split("#")[1]):
        return await _.answer_callback_query(query.id,"Not for you.")
    if (len(LOCATION) -1) - 1 == index :
        print((len(LOCATION) -1) -1)
        return await query.message.reply_photo(photo=LOCATION[index],caption="**Click on below button to set welcome image.**",
        reply_markup = InlineKeyboardMarkup([
            [ InlineKeyboardButton(
                    text=f"• Open •",
                    callback_data=f"open#{user_id}#{index}",
                ),
                InlineKeyboardButton(
                    text=f"• Back •",
                    callback_data=f"welbck#{user_id}:{index}",
                )
            ]
        ] ),
        )  
    else:
        return await query.message.reply_photo(photo=LOCATION[index],caption="**Click on below button to set welcome image.**",
        reply_markup = InlineKeyboardMarkup([
            [ InlineKeyboardButton(
                    text=f"• Back •",
                    callback_data=f"welbck#{user_id}#{index}",
                ),
                
                InlineKeyboardButton(
                    text=f"• Open •",
                    callback_data=f"open#{user_id}#{index}",
                ),
                InlineKeyboardButton(
                    text=f"• Next •",
                    callback_data=f"welnxt#{user_id}#{index}",
                )
            ]
        ] ),
        )  
@Client.on_callback_query(filters.regex(pattern=r"welbck#(.*)"))
async def _temp(_, query):
    await query.message.delete()
    chat_id = query.message.chat.id        
    user_id = query.from_user.id 
    index = int(query.data.split("#")[2]) - 1
    if user_id != int(query.data.split("#")[1]):
        return await _.answer_callback_query(query.id,"Not for you.")
    if index == 1 :
        return await query.message.reply_photo(photo=LOCATION[index],caption="**Click on below button to set welcome image.**",
        reply_markup = InlineKeyboardMarkup([
            [ InlineKeyboardButton(
                    text=f"• Open •",
                    callback_data=f"open#{user_id}#{index}",
                ),
                InlineKeyboardButton(
                    text=f"• Next •",
                    callback_data=f"welnxt#{user_id}:{index}",
                )
            ]
        ] ),
        )  
    else:
        return await query.message.reply_photo(photo=LOCATION[index],caption="**Click on below button to set welcome image.**",
        reply_markup = InlineKeyboardMarkup([
            [ InlineKeyboardButton(
                    text=f"• Back •",
                    callback_data=f"welbck#{user_id}#{index}",
                ),
                
                InlineKeyboardButton(
                    text=f"• Open •",
                    callback_data=f"open#{user_id}#{index}",
                ),
                InlineKeyboardButton(
                    text=f"• Next •",
                    callback_data=f"welnxt#{user_id}#{index}",
                )
            ]
        ] ),
        )    
@Client.on_message(filters.command("rmwelcome") & filters.group)
@user_admin
@user_can_change_info
async def _delwel(_, message):
    chat_id = message.chat.id
    bsdk = await is_welcome_on(chat_id)
    if not bsdk:
        await message.reply_text("**Welcome template isn't enabled.**")
    del_welcome(chat_id)
    await message.reply_text("**Welcome template disabled.**")
        



    
