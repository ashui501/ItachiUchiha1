import time
import re
from pyrogram import filters, enums, Client
from pyrogram.types import Message
from Itachi.modules.mongo.afk_db import add_afk, cleanmode_off, cleanmode_on, is_afk, remove_afk
from Itachi import *
from Itachi.modules.pyro.status import user_admin
from Itachi import get_readable_time as get_readable_time2
from datetime import datetime, timedelta


cleanmode = {}
async def put_cleanmode(chat_id, message_id):
    if chat_id not in cleanmode:
        cleanmode[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=1),
    }
    cleanmode[chat_id].append(put)

@Client.on_message(filters.command(["afk" , "brb"]))
@Client.on_message(filters.regex("brb"))
@Client.on_message(filters.regex("Brb"))
async def active_afk(self: app, ctx: Message):
    if ctx.sender_chat:
        return await ctx.reply_text("**Channels can't be afk!**")
    user_id = ctx.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            if afktype == "animation":
                send = (
                    await ctx.reply_animation(
                        data,
                        caption="{} was afk for {}.".format(ctx.from_user.mention, seenago),
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_animation(
                        data,
                        caption="{} was afk for {}.\nreason : {}".format(ctx.from_user.mention, seenago, reasonafk),
                    )
                )
            elif afktype == "photo":
                send = (
                    await ctx.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption="{} was afk for {}.".format(ctx.from_user.mention, seenago),
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption="{} was afk for {}.\nreason : {}".format(ctx.from_user.first_name, seenago, reasonafk),
                    )
                )
            elif afktype == "text":
                send = await ctx.reply_text(
                    caption="{} was afk for {}.".format(ctx.from_user.mention,  seenago),
                    disable_web_page_preview=True,
                )
            elif afktype == "text_reason":
                send = await ctx.reply_text(
                    caption="{} was afk for {}.\nreason : {}".format(ctx.from_user.mention, seenago, reasonafk),
                    disable_web_page_preview=True,
                )
        except Exception:
            send = await ctx.reply_text(
                "{} is back!".format(ctx.from_user.first_name),
                disable_web_page_preview=True,
            )
        await put_cleanmode(ctx.chat.id, send.id)
        return
    if len(ctx.command) == 1 and not ctx.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and not ctx.reply_to_message:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        _reason = ctx.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.sticker:
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif len(ctx.command) > 1 and ctx.reply_to_message.sticker:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
    send = await ctx.reply_text("{} is now afk!".format(ctx.from_user.mention))
    await put_cleanmode(ctx.chat.id, send.id)


@Client.on_message(filters.command("afkdel") & filters.group)
@user_admin
async def afk_state(self: app, ctx: Message):
    if not ctx.from_user:
        return
    chat_id = ctx.chat.id
    state = ctx.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await cleanmode_on(chat_id)
        await ctx.reply_text("afk delete enbled!")
    elif state == "disable":
        await cleanmode_off(chat_id)
        await ctx.reply_text("afk delete disabled!")

# Detect user that AFK based on Yukki Repo
@Client.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=11,
)
async def chat_watcher_func(self: app, ctx: Message):
    if ctx.sender_chat:
        return
    userid = ctx.from_user.id
    user_name = ctx.from_user.mention
    if ctx.entities:
        possible = ["/afk", f"/afk@{self.me.username}", "!afk"]
        message_text = ctx.text or ctx.caption
        for entity in ctx.entities:
            if entity.type == enums.MessageEntityType.BOT_COMMAND:
                if (message_text[0 : 0 + entity.length]).lower() in possible:
                    return

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            if afktype == "text":
                msg += "{} was afk for {}.".format(user_name, seenago)
            if afktype == "text_reason":
                msg += "{} was afk for {}.\nreason : {}".format(user_name, seenago, reasonafk)
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await ctx.reply_animation(
                        data,
                        caption="{} was afk for {}.".format(user_name, seenago),
                    )
                else:
                    send = await ctx.reply_animation(
                        data,
                        caption="{} was afk for {}.\nreason : {}".format(user_name, seenago, reasonafk),
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await ctx.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption="{} is afk for {}.".format(user_name, seenago),
                    )
                else:
                    send = await ctx.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption="{} is afk for {}.\nreason : {}".format(user_name, seenago, reasonafk),
                    )
        except:
            msg += "{} is back!".format(user_name)

    # Replied to a User which is AFK
    if ctx.reply_to_message:
        try:
            replied_first_name = ctx.reply_to_message.from_user.mention
            replied_user_id = ctx.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time2((int(time.time() - timeafk)))
                    if afktype == "text":
                        msg += "{} is afk for {}.".format(replied_first_name, seenago)
                    if afktype == "text_reason":
                        msg += "{} is afk for {}.\nreason : {}".format(replied_first_name, seenago, reasonafk)
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            send = await ctx.reply_animation(
                                data,
                                caption="{} is afk for {}.".format(replied_first_name, seenago),
                            )
                        else:
                            send = await ctx.reply_animation(
                                data,
                                caption="{} is afk for {}.\nreason : {}".format(replied_first_name, seenago, reasonafk),
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            send = await ctx.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption="{} is afk for {}.".format(replied_first_name, seenago),
                            )
                        else:
                            send = await ctx.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption="{} is afk for {}.\nreason : {}".format(replied_first_name, seenago, reasonafk),
                            )
                except Exception:
                    msg += "{} is afk right now!".format(replied_first_name)
        except:
            pass

    # If username or mentioned user is AFK
    if ctx.entities:
        entity = ctx.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == enums.MessageEntityType.MENTION:
                found = re.findall("@([_0-9a-zA-Z]+)", ctx.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time2((int(time.time() - timeafk)))
                        if afktype == "text":
                            msg += "{} is afk for {}.".format(user.first_name[:25], seenago)
                        if afktype == "text_reason":
                            msg += "{} is afk for {}.\nreason : {}".format(user.first_name[:25], seenago,reasonafk)
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_animation(
                                    data,
                                    caption="{} is afk for {}.".format(user.first_name[:25], seenago),
                                )
                            else:
                                send = await ctx.reply_animation(
                                    data,
                                    caption="{} is afk for {}.\nreason : {}".format(user.first_name[:25], seenago, reasonafk),
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption="{} is afk for {}.".format(user.first_name[:25], seenago),
                                )
                            else:
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption="{} is afk for {}.\nreason : {}".format(user.first_name[:25], seenago, reasonafk),
                                )
                    except:
                        msg += "{} is afk!".format(user.first_name[:25])
            elif (entity[j].type) == enums.MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time2((int(time.time() - timeafk)))
                        if afktype == "text":
                            msg += "{} is afk for {}.".format(first_name[:25], seenago)
                        if afktype == "text_reason":
                            msg += "{} was afk for {}.\nreason : {}".format(first_name[:25], seenago, reasonafk)
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_animation(
                                    data,
                                    caption="{} was afk for {}.".format(first_name[:25], seenago),
                                )
                            else:
                                send = await ctx.reply_animation(
                                    data,
                                    caption="{} was afk for {}.\nreason : {}".format(first_name[:25], seenago, reasonafk),
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption="{} was afk for {}.".format(first_name[:25], seenago),
                                )
                            else:
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption="{} was afk for {}.\nreason : {}".format(first_name[:25],seenago, reasonafk),
                                )
                    except:
                        msg += "{} is afk!".format(first_name[:25])
            j += 1
    if msg != "":
        try:
            send = await ctx.reply_text(msg, disable_web_page_preview=True)
        except:
            pass
    try:
        await put_cleanmode(ctx.chat.id, send.id)
    except:
        pass

__help__ = """
**Here is The Help For Afk**

**Commands**
 /afk - This will set you offline.

 /afk [reason] - This will set you offline with a reason.

 /afk [reply to sticker/photo] - This will set you offline with a photo or sticker.

 /afk [reply to sticker/photo] [reason] - This will set you offline with a photo or sticker with a reason.
"""
__mod_name__ = "Afk"
