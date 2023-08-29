from pyrogram import Client, filters , enums


@Client.on_message(filters.command("id"))
async def djjxnx(_,message):
    replied = message.reply_to_message
    user = message.from_user
    if replied:
        return await message.reply_text(f"**{replied.from_user.mention}** Your ID is : `{replied.from_user.id}`")
    if message.chat.type ==  enums.ChatType.PRIVATE:
        return await message.reply_text(f"**{message.from_user.mention}** Your ID is : `{message.from_user.id}`")
    await message.reply_text(f"**ID of this Chat Group is** : `{message.chat.id}`")
