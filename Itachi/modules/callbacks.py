import os
import time
import random
import psutil
import strings
from strings import *
import platform
from pyrogram import filters , __version__ as pyro , Client , enums , Client
from Itachi.modules.mongo.users_db import get_served_users
from Itachi.modules.mongo.chats_db import get_served_chats
from Itachi import app,StartTime,BOT_NAME,get_readable_time,BOT_USERNAME
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from .pyro.decorators import control_user
                       
STATS_MSG="""
────「 Itachi Uchiha 」────

• Uptime : {}
• Users : {}
• Chats : {}
• Bot : {} MB
• Ram : {}%
• Disk : {}%
• Processor : {}
• Server : {}
"""
ADMIN_M = """
✅Admin Commands:

c stands for channel play.

/pause or /cpause - Pause the playing music.
/resume or /cresume- Resume the paused music.
/mute or /cmute- Mute the playing music.
/unmute or /cunmute- Unmute the muted music.
/skip or /cskip- Skip the current playing music.
/stop or /cstop- Stop the playing music.
/shuffle or /cshuffle- Randomly shuffles the queued playlist.
/seek or /cseek - Forward Seek the music to your duration
/seekback or /cseekback - Backward Seek the music to your duration
/restart - Restart bot for your chat .


✅Specific Skip:
/skip or /cskip [Number(example: 3)] 
    - Skips music to a the specified queued number. Example: /skip 3 will skip music to third queued music and will ignore 1 and 2 music in queue.

✅Loop Play:
/loop or /cloop [enable/disable] or [Numbers between 1-10] 
    - When activated, bot loops the current playing music to 1-10 times on voice chat. Default to 10 times."""

PLAY_M = """
✅Play Commands:

Available Commands = play , vplay , cplay

ForcePlay Commands = playforce , vplayforce , cplayforce

c stands for channel play.
v stands for video play.
force stands for force play.

/play or /vplay or /cplay  - Bot will start playing your given query on voice chat or Stream live links on voice chats.

/playforce or /vplayforce or /cplayforce -  Force Play stops the current playing track on voice chat and starts playing the searched track instantly without disturbing/clearing queue.

/channelplay [Chat username or id] or [Disable] - Connect channel to a group and stream music on channel's voice chat from your group.


✅Bot's Server Playlists:
/playlist  - Check Your Saved Playlist On Servers.
/deleteplaylist - Delete any saved music in your playlist
/play  - Start playing Your Saved Playlist from Servers."""

music = """
Click on the buttons below for more information. If you're facing any problem in command you can contact my bot owner or ask in support chat.

All commands can be used with: /"""

ai_help_lol = """
**Artificial Intelligence Programs**

♠ `/ask` : powerful gpt4 fastest response rate.
♠ `/draw` : create artificial pictures.
♠ `/upscale` : increase quality of any picture.
♠ `/llama` : powerful Facebook meta ai text
"""


@Client.on_callback_query(filters.regex("friday_back"))
@control_user()
async def Friday(_, callback_query : CallbackQuery):
    query= callback_query.message
    mention=callback_query.from_user.mention
    uptime= get_readable_time((time.time() - StartTime))
    await query.edit_caption(strings.PM_START_TEXT.format(BOT_NAME,mention,uptime,platform.python_version(),pyro),
    reply_markup=InlineKeyboardMarkup(strings.START_BUTTONS))


@Client.on_callback_query(filters.regex(r"^(admin_music|play_music|music_p|m_back|ai_help)$"))
@control_user()
async def musics(client , callback_query : CallbackQuery):
    data = callback_query.data
    query = callback_query.message
    if data == "admin_music":
        return await query.edit_caption(ADMIN_M , reply_markup=InlineKeyboardMarkup(MUSIC_BACK))
    elif data == "play_music":
        return await query.edit_caption(PLAY_M , reply_markup=InlineKeyboardMarkup(MUSIC_BACK))
    elif data == "music_p":
        return await query.edit_caption(music , reply_markup=InlineKeyboardMarkup(MUSIC_BTN))
    elif data == "m_back":
        return await query.edit_caption(music , reply_markup=InlineKeyboardMarkup(MUSIC_BTN))
    elif data == "ai_help":
        return await query.edit_caption(ai_help_lol , reply_markup=InlineKeyboardMarkup(BACK_BTN))
    else:
        return 

@Client.on_callback_query(filters.regex("Friday_st"))
@control_user()
async def Fridays(client, callback_query : CallbackQuery):    
    uptime= get_readable_time((time.time() - StartTime))   
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    process = psutil.Process(os.getpid())
    processor = platform.processor()
    server = platform.system()
    mb= round(process.memory_info()[0] / 1024 ** 2)
    await client.answer_callback_query(
    callback_query.id,
    text=STATS_MSG.format(uptime,users,chats,mb,ram,disk,processor,server),
    show_alert=True
)


@Client.on_callback_query(filters.regex("admin_close"))
@control_user()
async def _close(client : Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    member = await client.get_chat_member(chat_id,user_id)
    if member.privileges:
            await query.message.delete()
            try:
                await query.message.reply_to_message.delete()
            except:
                pass
    else:
        await client.answer_callback_query(
        query.id,
        text = "You Don't Have Permission To Do This.",
        show_alert = True)
