from pyrogram import Client, filters
from Itachi import *
import httpx

url = "https://alphacoder-api-93747976af25.herokuapp.com"

@Client.on_message(filters.command("draw"))
async def gen_img(client, message):
    temp = await message.reply_text("**Creating, please wait for a minute...**")
    prompt = message.text.split(maxsplit=1)[1]
    data = {"prompt": prompt}
    async with httpx.AsyncClient(timeout=30) as cli:
        try:
            response = await cli.post(f"{url}/text2img", json=data)
            pic = response.json().get("output_url")
            await client.send_photo(message.chat.id, photo=pic, caption=f"**{message.from_user.mention} Here is your image.\nPrompt:** `{prompt}`")
            await temp.delete()
        except Exception as e:
            await temp.edit_text(f"**An error occurred:\n**`{str(e)}`")
