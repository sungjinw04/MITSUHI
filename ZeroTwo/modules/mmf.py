import asyncio
import logging
import os
import shlex
import textwrap
from typing import Tuple
from pyrogram import filters

from ZeroTwo import pgram as app

from PIL import Image, ImageDraw, ImageFont

absen = [
    "**Hadir bang** 😁",
    "**Hadir kak** 😉",
    "**Hadir dong** 😁",
    "**Hadir ganteng** 🥵",
    "**Hadir bro** 😎",
    "**Hadir kak maap telat** 🥺",
]

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

async def add_text_img(image_path, text):
    font_size = 13
    stroke_width = 2

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="ZeroTwo/LOGO_FONT/default (4).ttf",
        size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    bbox = font.getbbox("A")
    char_width, char_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            bbox = font.getbbox(line)
            line_width, line_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            bbox = font.getbbox(line)
            line_width, line_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = os.path.join("memify.webp")
    img.save(final_image, **img_info)
    return final_image


# https://github.com/TeamUltroid/pyUltroid/blob/31c271cf4d35ab700e5880e952e54c82046812c2/pyUltroid/functions/helper.py#L154

@app.on_message(filters.command(["mmf", "memify"]), group = 10)
async def memify(client, message):
    if message.reply_to_message and (message.reply_to_message.sticker or message.reply_to_message.photo):
        try:
            file = await message.reply_to_message.download()
            res = await add_text_img(file, message.text.split(None, 1)[1].strip())
            await message.reply_sticker(res)
            try:
                os.remove(res)
            except Exception as e:
                logging.error("Error removing file: %s", str(e))
        except Exception as e:
            logging.error("Error in memify function: %s", str(e))
            await message.reply("Use the <b>/mmf <text></b> command with a reply to the sticker, separated by ; to make the position of the text below.")
    else:
        await message.reply("Use the <b>/mmf <text></b> command with a reply to the sticker, separated by ; to make the position of the text below.")
        
__help__ = """
❍ */mmf or /memify <text> :* Use the /mmf or /memify command with a reply to the sticker, separated by ; to make the position of the text below. You can write texts on image or sticker with the help of this awesome command.
"""

__mod_name__ = "𝙼ᴇᴍɪғʏ"
  
