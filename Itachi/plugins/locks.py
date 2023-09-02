import asyncio
from Itachi import app
from Itachi.config import SUPER_USERS as CHAD
from pyrogram import filters , Client
from Itachi.modules.mongo.approve_db import approved_users
from Itachi.modules.pyro.permissions import *
from pyrogram.types import ChatPermissions
from pyrogram.errors import ChatAdminRequired, ChatNotModified

AVAILABLE_LOCKS = """
**★ Locks Available:**

× all
× msg
× media
× polls
× invite
× pin
× info
× webprev
× inline
× animations
× games
× stickers
"""

async def convert_to_emoji(value: bool):
        if value:
            return "✅"
        return "❌"


@Client.on_message(filters.command("locktypes") & filters.group)
async def _locktypes(_, message):
    return await message.reply_text(AVAILABLE_LOCKS)


@Client.on_message(filters.command("locks") & filters.group)
async def _locks(_, message):
    admin = is_admin(message.chat.id , message.from_user.id)
    if not admin:
        return await message.reply_text("**You aren't an admin.**")
    msg = await message.reply("**checking...**")
    permissions = message.chat.permissions
    msgs = await convert_to_emoji(permissions.can_send_messages)
    medias = await convert_to_emoji(permissions.can_send_media_messages)
    others = await convert_to_emoji(permissions.can_send_other_messages)
    webprevs = await convert_to_emoji(permissions.can_add_web_page_previews)
    polls = await convert_to_emoji(permissions.can_send_polls)
    infos = await convert_to_emoji(permissions.can_change_info)
    invites = await convert_to_emoji(permissions.can_invite_users)
    pins = await convert_to_emoji(permissions.can_pin_messages)
    if permissions:
        try:
            chat_locks = "**★ Permissions :**\n\n"
            chat_locks += f"**• Send Messages** : {msgs}\n"
            chat_locks += f"**• Send Media **: {medias}\n"
            chat_locks += f"**• Send Stickers** : {others}\n"
            chat_locks += f"**• Send Animations** : {others}\n"
            chat_locks += f"**• Play Games** : {others}\n"
            chat_locks += f"**• Inline Bot** : {others}\n"
            chat_locks += f"**• Webpage Preview** : {webprevs}\n" 
            chat_locks += f"**• Polls** : {polls}\n"
            chat_locks += f"**• Change Info** : {infos}\n"
            chat_locks += f"**• Invite Users** : {invites}\n"
            chat_locks += f"**• Pin** : {pins}\n"
            return await msg.edit(chat_locks)  
        except Exception as e:
            await msg.edit(e)    
    
@Client.on_message(filters.command("lock") & filters.group)
async def _lock(_, message):
    admin = is_admin(message.chat.id , message.from_user.id)
    if not admin:
        return await message.reply_text("**You aren't an admin.**")
    if len(message.command) < 2:
        return await message.reply_text("**Usage:** `/lock name`")
    chat_id = message.chat.id
    lock_type = message.text.split()[1].lower()
    
    get_perm = message.chat.permissions
    msg = get_perm.can_send_messages
    media = get_perm.can_send_media_messages
    webprev = get_perm.can_add_web_page_previews
    polls = get_perm.can_send_polls
    info = get_perm.can_change_info
    invite = get_perm.can_invite_users
    pin = get_perm.can_pin_messages
    stickers = animations = games = inlinebots = None
    
    if lock_type == "all":
        try:
            await _.set_chat_permissions(chat_id, ChatPermissions())            
        except ChatNotModified:
            pass
        except ChatAdminRequired:
            return await message.reply_text("**I don't have permission to do that.**")
        await message.reply_text("**🔐 Locked All Permissions From Chat.**")
        await prevent_approved(_, message)
        return

    if lock_type == "msg":
        msg = False
        perm = "messages"

    elif lock_type == "media":
        media = False
        perm = "audios, documents, photos, videos, video notes, voice notes"

    elif lock_type == "stickers":
        stickers = False
        perm = "stickers"

    elif lock_type == "animations":
        animations = False
        perm = "animations"

    elif lock_type == "games":
        games = False
        perm = "games"

    elif lock_type in ("inlinebots", "inline"):
        inlinebots = False
        perm = "inline bots"

    elif lock_type == "webprev":
        webprev = False
        perm = "web page previews"

    elif lock_type == "polls":
        polls = False
        perm = "polls"

    elif lock_type == "info":
        info = False
        perm = "info"

    elif lock_type == "invite":
        invite = False
        perm = "invite"

    elif lock_type == "pin":
        pin = False
        perm = "pin"

    else:
        return await messsage.reply_text("**Invalid Locktypes.**")
                            
    try:
        await _.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=msg,
                can_send_media_messages=media,
                can_send_other_messages=any([stickers, animations, games, inlinebots]),
                can_add_web_page_previews=webprev,
                can_send_polls=polls,
                can_change_info=info,
                can_invite_users=invite,
                can_pin_messages=pin,
            ),
        )        
    except ChatNotModified:
        pass
    except ChatAdminRequired:
        await message.reply_text("**I don't have permission to do that.**")
    await message.reply_text(f"**🔐 Locked {perm} For This Chat!**")           
    await prevent_approved(_, message)
    return

async def prevent_approved(app,message):
    chat_id = message.chat.id
    list_approved = await approved_users(chat_id) + CHAD  
    print(list_approved)  
    for i in list_approved:
        try:
            await app.unban_chat_member(chat_id,int(i))
        except Exception as e:
            print(e)        
        await asyncio.sleep(0.1)
    return    
         
@Client.on_message(filters.command("unlock") & filters.group)
async def unlock_perm(_, message):
    admin = is_admin(message.chat.id , message.from_user.id)
    if not admin:
        return await message.reply_text("**You aren't an admin.**")
    if len(message.command) < 2:
        await m.reply_text("**Usage**: `/unlock name`")
        return
    unlock_type = message.text.split()[1].lower()
    chat_id = message.chat.id
    
    if unlock_type == "all":
        try:
            await _.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                ),
            )          
        except ChatNotModified:
            pass
        except ChatAdminRequired:
            return await message.reply_text("**I don't have permission to do that.**")
        await message.reply_text("**🔓 Unlocked All Permission in this chat.**")
        await prevent_approved(_, message)
        return

    get_uperm = message.chat.permissions
    umsg = get_uperm.can_send_messages
    umedia = get_uperm.can_send_media_messages
    uwebprev = get_uperm.can_add_web_page_previews
    upolls = get_uperm.can_send_polls
    uinfo = get_uperm.can_change_info
    uinvite = get_uperm.can_invite_users
    upin = get_uperm.can_pin_messages
    ustickers = uanimations = ugames = uinlinebots = None

    if unlock_type == "msg":
        umsg = True
        uperm = "messages"

    elif unlock_type == "media":
        umedia = True
        uperm = "audios, documents, photos, videos, video notes, voice notes"

    elif unlock_type == "stickers":
        ustickers = True
        uperm = "stickers"

    elif unlock_type == "animations":
        uanimations = True
        uperm = "animations"

    elif unlock_type == "games":
        ugames = True
        uperm = "games"

    elif unlock_type in ("inlinebots", "inline"):
        uinlinebots = True
        uperm = "inline bots"

    elif unlock_type == "webprev":
        uwebprev = True
        uperm = "web page previews"

    elif unlock_type == "polls":
        upolls = True
        uperm = "polls"

    elif unlock_type == "info":
        uinfo = True
        uperm = "info"

    elif unlock_type == "invite":
        uinvite = True
        uperm = "invite"

    elif unlock_type == "pin":
        upin = True
        uperm = "pin"

    else:
        return await message.reply_text("**Invalid Locktype.**")
    try:        
        await _.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=umsg,
                can_send_media_messages=umedia,
                can_send_other_messages=any(
                    [ustickers, uanimations, ugames, uinlinebots],
                ),
                can_add_web_page_previews=uwebprev,
                can_send_polls=upolls,
                can_change_info=uinfo,
                can_invite_users=uinvite,
                can_pin_messages=upin,
            ),
        )
    except ChatNotModified:
        pass
    except ChatAdminRequired:
        return await messagd.reply_text("**I don't have permission to do that.**")
    await message.reply_text(f"**🔓 Unlocked {uperm} for this chat.**")
    await prevent_approved(m)
    return
