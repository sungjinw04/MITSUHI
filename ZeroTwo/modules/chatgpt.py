import json
import requests
import httpx
import time

from pyrogram import filters
from pyrogram.enums import ChatAction, ParseMode

from ZeroTwo import pgram, aiohttpsession, BOT_USERNAME


@pgram.on_message(filters.command(["chatgpt","ai","ask"]))
async def chat(client, message):
    try:
        start_time = time.time()
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "Example:**\n\n`/chatgpt Where is TajMahal?`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/chatgpt?query={a}') 
            x=response.json()["results"]
            end_time = time.time()
            telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ᴍs"
            await message.reply_text(f" {x}\n\n✨ᴛɪᴍᴇ ᴛᴀᴋᴇɴ  {telegram_ping} \n\n🎉ᴘᴏᴡᴇʀᴇᴅ ʙʏ @{BOT_USERNAME} ", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ: {e} ")
        
