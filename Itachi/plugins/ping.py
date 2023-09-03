import time
import asyncio 
from typing import List
from Itachi import app,get_readable_time,StartTime
from Itachi.config import DEV_USERS
from pyrogram import filters , Client
from httpx import AsyncClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


@Client.on_message(filters.command("ping"))
async def _ping(_, message):
    start = time.time()
    msg = await message.reply("⚡")
    end = time.time()
    telegram_ping = str(round((end - start) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - StartTime)) + "uptime"
    await msg.edit(f"""
**• Ping  •
» {telegram_ping}
» {uptime}**""")

