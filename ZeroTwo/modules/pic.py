from telethon import *
from telethon.tl.functions.account import *
from telethon.tl.functions.channels import *
from telethon.tl.functions.photos import *
from telethon.tl.types import *
from ZeroTwo.events import register
from ZeroTwo import tbot as borg
from html import *
import logging

logger = logging.getLogger(__name__)

@register(pattern=("/pic"))
async def PPScmd(event):
    try:
        user = await event.get_reply_message()
        if user:
            # Fetch only the 5 most recent photos
            photos = await event.client.get_profile_photos(user.sender, limit=5)
        else:
            # Fetch only the 5 most recent photos
            photos = await event.client.get_profile_photos(event.chat_id, limit=5)

        if not photos:
            await event.reply("No photos found.")
            return
        
        # Prepare a list to hold the file references
        media = []
        for photo in photos:
            media.append(photo)

        # Sending the photos as a group (album)
        await borg.send_file(event.chat.id, media)

    except Exception as e:
        logger.error(e)  # Log the error
        await event.reply("An error occurred. Please try again.")
        
