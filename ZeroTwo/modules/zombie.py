import asyncio
from telethon import events
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins

from ZeroTwo import tbot as telethn
from ZeroTwo import DRAGONS

# =================== CONSTANT ===================
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

OFFICERS = DRAGONS

async def is_administrator(user_id: int, chat_id):
    admin = False
    async for user in telethn.iter_participants(
        chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in OFFICERS:
            admin = True
            break
    return admin

@telethn.on(events.NewMessage(pattern="^[!/]zombies ?(.*)"))
async def rm_deletedacc(event):
    user_id = event.sender_id
    chat_id = event.chat_id
    is_admin = await is_administrator(user_id, chat_id)
    
    if not is_admin:
        await event.reply("**Sorry, you must be an admin to use this command.**")
        return

    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**Group clean, 0 deleted accounts found.**"
    if con != "clean":
        message = await event.reply("`Searching for deleted account to remove...`")
        async for user in event.client.iter_participants(chat_id):
            if user.deleted:
                del_u += 1
                await asyncio.sleep(1)  # proper use of asyncio's sleep function
        if del_u > 0:
            del_status = f"**Searching...** `{del_u}` **Deleted account/Zombie in this group,**\n**Clean it with command** `/zombies clean`"
        return await message.edit(del_status)

    # Code to remove deleted accounts
    chat = await event.get_chat()
    if not (chat.admin_rights and chat.admin_rights.ban_users) and not chat.creator:
        return await event.reply("**Sorry you're not admin!**")
    message = await event.reply("`Removing deleted accounts...`")
    del_u = 0
    del_a = 0
    async for user in telethn.iter_participants(chat_id):
        if user.deleted:
            try:
                await event.client(EditBannedRequest(chat_id, user.id, BANNED_RIGHTS))
                await event.client(EditBannedRequest(chat_id, user.id, UNBAN_RIGHTS))
                del_u += 1
            except ChatAdminRequiredError:
                await message.edit("`I do not have ban rights in this group.`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1

    del_status = f"**Cleaned** `{del_u}` **Zombies**"
    if del_a > 0:
        del_status += f"\n`{del_a}` **Admin zombies not deleted.**"
    await message.edit(del_status)
                
