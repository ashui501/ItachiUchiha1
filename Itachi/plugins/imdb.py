import requests
from Itachi import app as pgram
from pyrogram import filters , Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MediaEmpty , BadRequest 

    
@Client.on_message(filters.command("imdb"))
async def ntg(_, message):
    msg = await message.reply("**🔍 Searching......**")
    if len(message.command) < 2 :
        await msg.edit("**give me a query**")
    q = message.text.split(None,1)[1]
    k = requests.get(f"https://api.safone.me/tmdb?query={q}%20&limit=10").json()
    im = k["results"]    
    if not im:
        await msg.edit("refine your search 🔍.")
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('releaseDate').split('-')[0]}",
                    callback_data=f"imdb#{movie.get('id')}",
                )
            ]
            for movie in im
        ]
    await msg.edit('💝 Here is what i found in IMDB.', reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(pattern=r"imdb#(.*)"))
async def IMDb_cb(_, query):
    msg = await query.message.edit_text("**🔍 Searching.........**")
    id = int(query.data.split("#")[1])
    tmdb = requests.get(f"https://api.safone.me/tmdb?query=%20&tmdb_id={id}").json() 
    imdb = tmdb["results"][0]
    text = f"📀 **Title :** {imdb['title']}\n\n"
    text += f"⏱️ **Runtime :** {imdb['runtime']}ᴍɪɴ\n"
    text += f"🌟 **Rating :** {imdb['rating']}/10\n" 
    text += f"🗳️ **ID :** {imdb['id']}\n\n"
    text += f"📆 **Release Date :** {imdb['releaseDate']}\n"
    text += f"🎭 **Genre :** \n"
    for x in imdb['genres']:
            text += f"{x}, "
    text = text[:-2] + '\n'
    text += f"🥂 **Popularity :** {imdb['popularity']}\n\n"
    text += f"⚡ **Status :** {imdb['status']}\n"
    text += f"🎫 **IMDB ID :** {imdb['imdbId']}\n\n"
    text += f"🗒  **Plot :** `{imdb['overview']}`"
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🎟️ IMDB",url=imdb["imdbLink"])]])
    try :
        if imdb["poster"]:
            await query.message.reply_photo(photo=imdb["poster"], caption=text,reply_markup=buttons)
        else:
            await query.message.reply_text(text,reply_markup=buttons)  
    except (MediaEmpty,BadRequest):
        await query.message.reply_text(text,reply_markup=buttons)    
    except Exception as a:
        await query.message.reply_text("**something went wrong.**") 
        print(a)  
    await msg.delete()     
    
        


__help__="""
「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
๏ /IMDb «ᴍᴏᴠɪᴇ ɴᴀᴍᴇ» : ɢᴇᴛ ғᴜʟʟ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴀ ᴍᴏᴠɪᴇ ғʀᴏᴍ ɪᴍᴅʙ.ᴄᴏᴍ
═───────◇───────═
"""  
__mod_name__ = "𝙸ᴍᴅʙ"
