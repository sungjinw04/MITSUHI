from requests import get
from ZeroTwo import pgram as pbot
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
from ZeroTwo.utils.permissions import adminsOnly
from pymongo import MongoClient

client = MongoClient("mongodb+srv://zerotwo:zerotwo@cluster0.mtn4wgj.mongodb.net/?retryWrites=true&w=majority")
db = client["mydatabase"]
collection = db["pinterest_command"]

@pbot.on_message(filters.command(["pinterest", "pint"]))
async def pinterest(_, message):
    chat_id = message.chat.id
    document = collection.find_one({"chat_id": chat_id})

    if document is None or document.get("status", True):
        try:
            query = message.text.split(None, 1)[1]
        except:
            return await message.reply("Please enter an image name to search 🔍")

        images = get(f"https://pinterest-api-one.vercel.app/?q={query}").json()

        images_url = images["images"][:6]

        media_group = []
        for url in images_url:
            media_group.append(InputMediaPhoto(media=url))

        try:
            return await pbot.send_media_group(
                chat_id=chat_id,
                media=media_group,
                reply_to_message_id=message.id)
        except Exception as e:
            return await message.reply(f"Error\n{e}")
    else:
        await message.reply("pinterest command is currently disabled in this chat.")

@pbot.on_message(filters.command("enablep"))
@adminsOnly("can_change_info")
async def enable_pinterest(client, message):
    chat_id = message.chat.id
    document = collection.find_one({"chat_id": chat_id})

    if document is None:
        # Document doesn't exist, create a new one with status=True
        collection.insert_one({"chat_id": chat_id, "status": True})
        await message.reply("pinterest command has been enabled.")
    else:
        status = document.get("status", True)
        if status:
            await message.reply("pinterest command is already enabled in this chat.")
        else:
            collection.update_one({"chat_id": chat_id}, {"$set": {"status": True}})
            await message.reply("pinterest command has been enabled.")

@pbot.on_message(filters.command("disablep"))
@adminsOnly("can_change_info")
async def disable_pinterest(client, message):
    chat_id = message.chat.id
    document = collection.find_one({"chat_id": chat_id})

    if document is None:
        # Document doesn't exist, create a new one with status=False
        collection.insert_one({"chat_id": chat_id, "status": False})
        await message.reply("pinterest command has been disabled.")
    else:
        status = document.get("status", True)
        if not status:
            await message.reply("pinterest command is already disabled in this chat.")
        else:
            collection.update_one({"chat_id": chat_id}, {"$set": {"status": False}})
            await message.reply("pinterest command has been disabled.")

__mod_name__ = "𝙸ᴍɢ 𝚂ᴇᴀʀᴄʜ"

__help__ = """
 ❍ /pinterest (your query): This command allows you to search and send up to 6 images related to your query from Pinterest. You can use /pint too to execute this command, Note that this command can be enabled or disabled by group admins using the /enablep and /disablep commands.

 ❍ /img (your query): When a user types /img (query), the bot will send 4 images related to that query from Google. For example, typing /img sakura will fetch and send 4 images of Sakura from Google. This command can be enabled or disabled by group admins using /enableimg or /disableimg.
 """
