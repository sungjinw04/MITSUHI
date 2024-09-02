import os
import shutil
import glob
import html

from pymongo import MongoClient
from telegram import ParseMode
from telethon.tl.types import ChannelParticipantsAdmins

from ZeroTwo import tbot
from ZeroTwo.events import register
from telegram.utils.helpers import mention_html

from bing_image_downloader import downloader

# Connect to MongoDB
client = MongoClient("mongodb+srv://zerotwo:zerotwo@cluster0.mtn4wgj.mongodb.net/?retryWrites=true&w=majority")
db = client["img_disable"]
collection = db["img_enable"]

async def is_command_enabled(chat_id):
    """
    Check if the /img command is enabled for the given chat_id.
    """
    result = collection.find_one({"chat_id": chat_id})
    return result is None or result.get("img_enabled", True)

async def is_admin(event):
    """
    Check if the user who triggered the event is an admin in a group or channel.
    """
    if event.chat_id > 0:  # Private chat
        return False

    chat = await event.get_chat()
    if not chat.admin_rights:
        return False

    participants = await event.client.get_participants(chat, filter=ChannelParticipantsAdmins)
    return any(participant.id == event.sender_id for participant in participants)


@register(pattern="^/img(?:\s+(.+))?$")
async def img_sampler(event):
    if event.fwd_from:
        return

    chat_id = event.chat_id
    if not await is_command_enabled(chat_id):
        await event.reply("⚠️ Sorry, the /img command is currently disabled for this group.")
        return

    query = event.pattern_match.group(1)
    if not query:
        await event.reply("❗️ Please provide a query to search for images.")
        return

    search_term = f'"{query}"'
    try:
        downloader.download(
            search_term,
            limit=4,
            output_dir="store",
            adult_filter_off=False,
            force_replace=False,
            timeout=60,
        )
    except Exception as e:
        await event.reply(f"❌ Failed to download images: {e}")
        return

    current_dir = os.getcwd()
    try:
        search_dir = os.path.join(current_dir, 'store', search_term)
        os.chdir(search_dir)
        types = ("*.png", "*.jpeg", "*.jpg")
        files_grabbed = []
        for file_type in types:
            files_grabbed.extend(glob.glob(file_type))
        if not files_grabbed:
            await event.reply("❌ Sorry, no images found for the given query.")
            return
        await tbot.send_file(event.chat_id, files_grabbed, reply_to=event.id)
    except Exception as e:
        await event.reply(f"❌ Error processing images: {e}")
    finally:
        os.chdir(current_dir)
        shutil.rmtree('store', ignore_errors=True)

@register(pattern="^/enableimg$")
async def enable_img(event):
    """
    Enable the /img command for the current chat.
    """
    if not event.is_group:
        await event.reply("⚠️ Sorry, this command can only be used in group chats.")
        return

    if not await is_admin(event):
        admin_mention = mention_html(event.sender_id, event.sender.first_name)
        await event.reply(f"{admin_mention}, ⚠️ Only admins can use this command.", parse_mode=ParseMode.HTML)
        return

    chat_id = event.chat_id
    result = collection.find_one({"chat_id": chat_id})
    if result and result.get("img_enabled", False):
        await event.reply("ℹ️ The /img command is already enabled for this group.")
    else:
        collection.update_one({"chat_id": chat_id}, {"$set": {"img_enabled": True}}, upsert=True)
        admin_mention = mention_html(event.sender_id, event.sender.first_name)
        await event.reply(f"✅ The /img command has been enabled for this group by {admin_mention}.", parse_mode=ParseMode.HTML)

@register(pattern="^/disableimg$")
async def disable_img(event):
    """
    Disable the /img command for the current chat.
    """
    if not event.is_group:
        await event.reply("⚠️ Sorry, this command can only be used in group chats.")
        return

    if not await is_admin(event):
        admin_mention = mention_html(event.sender_id, event.sender.first_name)
        await event.reply(f"{admin_mention}, ⚠️ Only admins can use this command.", parse_mode=ParseMode.HTML)
        return

    chat_id = event.chat_id
    result = collection.find_one({"chat_id": chat_id})
    if result and not result.get("img_enabled", True):
        await event.reply("ℹ️ The /img command is already disabled for this group.")
    else:
        collection.update_one({"chat_id": chat_id}, {"$set": {"img_enabled": False}}, upsert=True)
        admin_mention = mention_html(event.sender_id, event.sender.first_name)
        await event.reply(f"🚫 The /img command has been disabled for this group by {admin_mention}.", parse_mode=ParseMode.HTML)
