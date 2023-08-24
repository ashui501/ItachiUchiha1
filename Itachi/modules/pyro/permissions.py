from Itachi import app
from Itachi.config import SUPER_USERS
from pyrogram.enums import ChatMemberStatus, ChatType

async def is_group():
    if message.chat.type == ChatType.PRIVATE:
        return False
    return True

async def is_admin(chat, user):
    user_id = (await app.get_users(user)).id
    if user_id in SUPER_USERS:
        return True
    else:
        chat_member = await app.get_chat_member(chat, user)
        ctx = chat_member.privileges
        if ctx.can_delete_messages:
            return True
        elif ctx.can_manage_chat:
            return True
        elif ctx.can_manage_video_chats:
            return True
        elif ctx.can_restrict_members:
            return True
        elif ctx.can_promote_members:
            return True
        elif ctx.can_change_info:
            return True
        elif ctx.can_post_messages:
            return True
        elif ctx.can_edit_messages:
            return True
        elif ctx.can_invite_users:
            return True
        elif ctx.can_pin_messages:
            return True
        else:
            return False

async def can_promote(chat, user):
    check = (await app.get_chat_member(chat, user)).privileges.can_promote_members
    if not check:
        return False
    return True

async def can_delete(chat, user):
    check = (await app.get_chat_member(chat, user)).privileges.can_delete_messages
    if not check:
        return False
    return True

async def can_change_info(chat, user):
    check = (await app.get_chat_member(chat, user)).privileges.can_change_info
    if not check:
        return False
    return True

async def can_pin(chat, user):
    check = (await app.get_chat_member(chat, user)).privileges.can_pin_messages
    if not check:
        return False
    return True

async def can_invite(chat, user):
    check = (await app.get_chat_member(chat, user)).privileges.can_invite_users
    if not check:
        return False
    return True

async def can_restrict(chat, user):
    check = (await app.get_chat_member(chat, user)).privileges.can_restrict_members
    if not check:
        return False
    return True
