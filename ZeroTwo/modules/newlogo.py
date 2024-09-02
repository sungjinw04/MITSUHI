import os
import random
import glob
from blackpink import blackpink
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from ZeroTwo import pgram


@pgram.on_message(filters.command(["phlogo"]))
async def make_logog(client: Client, message: Message):
    msg = await message.reply("`processing...`")
    try:
        match = message.text.split(maxsplit=1)[1]
    except IndexError:
        return await msg.reply("`Provide a name to make logo...`")
    
    first = ""  # Initialize first with a default value
    if len(match.split()) >= 2:
        first, last = match.split()[:2]
    else:
        last = match
    
    logo = generate(first, last)
    name = "geezram.png"
    logo.save(name)
    await client.send_photo(
        message.chat.id, photo=name, reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None
    )
    os.remove(name)

@pgram.on_message(filters.command(["blink"]))
async def make_blink(client: Client, message: Message):
    msg = await message.reply("`processing...`")
    try:
        match = message.text.split(maxsplit=1)[1]
    except IndexError:
        return await msg.reply("`Provide a name to make logo...`")
    logo = blackpink(match)
    name = "geezram.png"
    logo.save(name)
    await client.send_photo(
        message.chat.id, photo=name, reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None
    )
    os.remove(name)

font=ImageFont.truetype("ZeroTwo/LOGO_FONT/IronFont.otf",110)
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im
    
def Gabung(fun):
    def gabung(arg):
        im,text1=add_corners(arg[0], 17),arg[1]
        op=Image.new("RGB",(40,20),color=(0,0,0))
        draw=ImageDraw.Draw(op)
        size=font.getsize(text1)
        baru=Image.new("RGB",(im.width+size[0]+210+20+130,600), color=(0,0,0))
        draw=ImageDraw.Draw(baru)
        draw.text((150,250), text1,(255,255,255),font=font)
        baru.paste(im, (150+size[0]+20,230+10), im.convert("RGBA"))
        return baru
    return gabung(fun)
    
def generate(text1, text2):
    panjangText=font.getsize(text2)
    oren=Image.new("RGBA",(panjangText[0]+20,140),color=(240, 152, 0))
    draw=ImageDraw.Draw(oren)
    draw.text((10,int((oren.height-panjangText[1])/2)-10),text2, (0,0,0),font=font)
    return Gabung([oren, text1])
