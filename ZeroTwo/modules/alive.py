import html
import asyncio
import random
from sys import version_info
import datetime
from datetime import datetime

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telegram import update
from telethon import __version__ as tver

from ZeroTwo import BOT_NAME
from ZeroTwo import OWNER_USERNAME, OWNER_NAME, SUPPORT_CHAT, pgram

PHOTO = [
    "https://graph.org//file/a9219e88a834c79e58370.jpg",
    "https://graph.org//file/de1dd3303dad1c7cb7dc4.jpg",
    "https://graph.org//file/1d77b8017265ddedff55e.jpg"
]

ASAU = [
    [
        InlineKeyboardButton(text="🚑Support", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
]

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)


@pgram.on_message(filters.command("alive"))
async def restart(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_video(
        random.choice(PHOTO),
        caption=f"""<b>✨I'm Alive Baby\n🥀I'm Working Perfectly</b>
     ▱▱▱▱▱▱▱▱▱▱▱▱
🔱<b>My Owner:</b> <a href="https://t.me/{OWNER_USERNAME}">{OWNER_NAME}</a>
🐍<b>Library Version:</b> <code>{lver}</code>
🤖<b>Bot Version: Stable</b>
⚡️<b>My Uptime:</b> <code>{uptime}</code>
     ▱▱▱▱▱▱▱▱▱▱▱▱""",
        reply_markup=InlineKeyboardMarkup(ASAU),
    )
