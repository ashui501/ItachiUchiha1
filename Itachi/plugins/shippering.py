from Itachi import app , db
from pyrogram import filters , Client
import random
from datetime import datetime
coupledb = db.couple

async def _get_lovers(chat_id: int):
    lovers = await coupledb.find_one({"chat_id": chat_id})
    if not lovers:
        return {}
    return lovers["couple"]

async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    return False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": chat_id},
        {"$set": {"couple": lovers}},
        upsert=True,
    )
CP_PIC = [
"https://graph.org/file/0f9583aa6fcb36991c38f.jpg",
 "https://graph.org/file/0cafa9cb2f1e9073da264.jpg",
 "https://graph.org/file/b4a56ceb9be9762a30a4f.jpg",
 "https://graph.org/file/f816de0ae59126e17291d.jpg",
 "https://graph.org/file/a36a298df4030cebec9ae.jpg",
]
# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())



@Client.on_message(filters.command("couples"))
async def couple(_, message):
    if message.chat.type == "private":
        await message.reply_text("This command only works in groups.")
        return
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in app.get_chat_members(message.chat.id):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                await message.reply_text("Not enough users")
                return
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await app.get_users(c1_id)).mention
            c2_mention = (await app.get_users(c2_id)).mention

            couple_selection_message = f"""**Couple of the day:**
{c1_mention} + {c2_mention} = 
__New couple of the day may be chosen at 12AM {tomorrow}__"""
            await app.send_photo(message.chat.id, photo=random.choice(CP_PIC),caption=couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name
            couple_selection_message = f"""Couple of the day:
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = 
__New couple of the day may be chosen at 12AM {tomorrow}__"""
            await app.send_photo(message.chat.id, photo=random.choice(CP_PIC),caption=couple_selection_message)
    except Exception as e:
        print(e)
        await message.reply_text(e)


