from Itachi import app 
from Itachi.config import BOT_TOKEN as bot_token , SUPPORT_CHAT
from pyrogram import filters , Client
from pyrogram.enums import ChatType
import requests
import json
import bs4
from urllib.parse import quote_plus
from collections import Counter
from bs4 import BeautifulSoup
from unidecode import unidecode
from pyrogram.enums import *
from pyrogram.types import *

async def Sauce(bot_token,file_id):
    r = requests.post(f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}').json()
    file_path = r['result']['file_path']
    headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
    to_parse = f"https://lens.google.com/uploadbyurl?url=https://api.telegram.org/file/bot{bot_token}/{file_path}"
    r = requests.get(to_parse,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    script_elements = soup.find_all('script')
    raw_data = [x for x in script_elements if 'Visual matches' in x.text]
    raw_data = raw_data[0].text
    start = raw_data.find('data:')+5
    end = raw_data.find('sideChannel') -2
    json_data = json.loads(raw_data[start:end])
    jason = []
    try:
        jason = json_data[1][1][1][8][8][0][12] if len(json_data[1]) == 2 else json_data[1][0][1][8][8][0][12]
    except:
        print("The data is not in the expected format")
    product_list = []
    for product in jason:
        information = {
            'google_image': product[0][0],
            'title': product[3],
            'redirect_url': product[5],
            'redirect_name': product[14],            
        }
        product_list.append(information)
    if product_list:
        most_common_product = product_list[0]  
        title = most_common_product['title']
        redirect_url = most_common_product['redirect_url']
        return {"title":title , "url":redirect_url}
    else:
        return False

async def get_file_id_from_message(msg):
    file_id = None
    message = msg.reply_to_message
    if not message:
        return 
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id
    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id
    if message.photo:
        file_id = message.photo.file_id
    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id
    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


@Client.on_message(filters.command(["pp","grs","reverse","p"]))
async def _reverse(_,msg):     
      text = await msg.reply("**⇢ wait a sec...**")
      file_id = await get_file_id_from_message(msg)
      if not file_id:
          return await text.edit("**reply to media!**")
      await text.edit("**⇢ Requesting to Google....**")    
      result = await Sauce(bot_token,file_id)
      if not result:
          return await text.edit(f"**API DOWN : @{SUPPORT_CHAT}**")
      await text.edit('**Result ⇢** [{}]({})'.format(result['title'] , result['url']),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support",url=f"t.me/{SUPPORT_CHAT}")]]))

      



 



 
