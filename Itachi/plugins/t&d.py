import requests
from Itachi import app
from pyrogram import filters , Client

@Client.on_message(filters.command(["truth","htruth"]))
async def true(_, message):
    if message.command[0] == "truth":
        url = "https://api.truthordarebot.xyz/v1/truth"
        truth = requests.get(url).json()["question"]
        await message.reply_text(f"`{truth}`")
        return 
    if message.command[0] == "htruth":
        url = "https://api.truthordarebot.xyz/v1/truth"
        truth = requests.get(url).json()["translations"]["hi"]
        await message.reply_text(f"`{truth}`")
        return     

@Client.on_message(filters.command(["dare","hdare"]))
async def _dare(_, message):
    if message.command[0] == "dare":
        url = "https://api.truthordarebot.xyz/v1/dare"
        dare = requests.get(url).json()["question"]
        await message.reply_text(f"`{dare}`")
        return 
    if message.command[0] == "hdare":
        url = "https://api.truthordarebot.xyz/v1/dare"
        dare = requests.get(url).json()["translations"]["hi"]
        await message.reply_text(f"`{dare}`")
        return 
