import os
import asyncio
import textwrap
import cv2

from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from Itachi import *

@app.on_message(filters.command("mmf"))
async def mmf(_, message):
    reply = message.reply_to_message
    msg = message.text[len("/mmf ") :]
    if not reply and reply.media:
       a = await message.reply_text("**REPLY TO ANY MEDIA**")
       return
    if not msg:
       a = await message.reply_text("**GIVE SOME TEXT**")
       return
    mda = await reply.download()
    if mda.endswith((".tgs")):
       a = message.reply_text("I SEE AN ANIMATED STKR...")
       cmd = ["lottie_convert.py", mda, "mmf.png"]
       file = "mmf.png"
       process = await asyncio.create_subprocess_exec(*cmd , stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
       stdout, stderr = await process.communicate()
       stderr.decode().strip()
       stdout.decode().strip()
    elif mda.endswith((".webp", ".png")):
       a = await message.reply_text("PROCESSING...")
       im = Image.open(mda)
       im.save("mmf.png", format="PNG", optimize=True)
       file = "mmf.png"
    else:
       a = await message.reply_text("PROCESSING...")
       img = cv2.VideoCapture(mda)
       heh, lol = img.read()
       cv2.imwrite("mmf.png", lol)
       file = "mmf.png"
    stick = await draw_meme_text(file, msg)
    await message.reply_document(stick)
    await a.delete()
    try:
        os.remove(mda)
        os.remove(file)
        os.remove(stick)
    except BaseException:
        pass


async def draw_meme_text(image_path, msg):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    if "_" in msg:
        text, font = msg.split("_")
    else:
        text = msg
        font = "default"
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = ImageDraw.Draw(img)
    m_font = ImageFont.truetype(
        f"resources/fonts/{font}.ttf", int((70 / 640) * i_width)
    )
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
            draw.text(
                xy=(((i_width - u_width) / 2) - 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 1,
                    i_height - u_height - int((80 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 1,
                    i_height - u_height - int((80 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((80 / 640) * i_width)) - 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((80 / 640) * i_width)) + 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((80 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    imag = "mmf.webp"
    img.save(imag, "WebP")
    return imag
