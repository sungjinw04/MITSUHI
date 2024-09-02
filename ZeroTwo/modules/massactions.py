from time import sleep

from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, ChatBannedRights, InputPeerChannel, InputChannel, InputPeerUser, ChannelParticipantsKicked, ChannelParticipantsBanned, UserStatusLastMonth
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest
from telethon.errors import UserNotParticipantError, FloodWaitError

from ZeroTwo import *
from ZeroTwo.events import register

async def is_register_admin(chat, user):
    if isinstance(chat, (InputPeerChannel, InputChannel)):
        return isinstance(
            (
                await tbot(GetParticipantRequest(chat, user))
            ).participant,
            (ChannelParticipantAdmin, ChannelParticipantCreator),
        )
    if isinstance(chat, InputPeerUser):
        return True



async def get_participant(chat_id, user_id):
    try:
        cutiepii = await tbot(GetParticipantRequest(chat_id, user_id))
        return cutiepii
    except UserNotParticipantError:
        return None


@register(pattern="^/unbanall$")
async def _(event):
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator
    if event.is_private:
        return await event.reply("__This command can be use in groups and channels!__")

    is_owner = False
    cutiepii = await get_participant(event.chat_id, event.sender_id)
    if cutiepii and isinstance(cutiepii.participant, ChannelParticipantCreator):
        is_owner = True

    if not is_owner:
        return await event.reply("__Only group owners can use this command!__")

    if not admin and not creator:
        await event.reply("`I don't have enough permissions!`")
        return

    done = await event.reply("Searching Participant Lists.")
    p = 0
    async for i in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await tbot(EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            LOGGER.warn(f"sleeping for {ex.seconds} seconds")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No one is banned in this chat")
        return
    required_string = "Successfully unbanned **{}** users"
    await event.reply(required_string.format(p))


@register(pattern="^/unmuteall$")
async def _(event):
    if event.is_private:
      return await event.reply("__This command can be use in groups and channels!__")

    is_admin = False
    try:
      cutiepii = await tbot(GetParticipantRequest(
        event.chat_id,
        event.sender_id
      ))
    except UserNotParticipantError:
      is_admin = False
    else:
      if (
        isinstance(
          cutiepii.participant,
          (
            ChannelParticipantAdmin,
            ChannelParticipantCreator,
          )
        )
      ):
        is_admin = True
    if not is_admin:
      return await event.reply("__Only admins can Unmuteall!__")
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator

    # Well
    if not admin and not creator:
        await event.reply("`I don't have enough permissions!`")
        return

    done = await event.reply("Working ...")
    p = 0
    async for i in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsBanned, aggressive=True
    ):
        rights = ChatBannedRights(
            until_date=0,
            send_messages=False,
        )
        try:
            await tbot(EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            LOGGER.warn(f"sleeping for {ex.seconds} seconds")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No one is muted in this chat")
        return
    required_string = "Successfully unmuted **{}** users"
    await event.reply(required_string.format(p))
    

@register(pattern="^/kickthefools")
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if event.is_private:
        return await event.reply("⚠️ This command can only be used in groups and channels! ⚠️")
    if not event.chat.admin_rights.ban_users:
        return
    is_owner = False
    cutiepii = await get_participant(event.chat_id, event.sender_id)
    if cutiepii and isinstance(cutiepii.participant, ChannelParticipantCreator):
        is_owner = True
    if not is_owner:
        return await event.reply("🚫 Only group owners have the privilege to use this command! 🚫")
    if not admin and not creator:
        await event.reply("❌ I'm sorry, I am not an admin in this group! ❌")
        return
    c = 0
    KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
    await event.reply("🔍 Searching the participant list...")
    async for i in event.client.iter_participants(event.chat_id):

        if isinstance(i.status, UserStatusLastMonth):
            status = await event.client(EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
                return
            else:
                c = c + 1
                    
        if isinstance(i.status, UserStatusLastMonth):
            status = await event.client(EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
                return
            else:
                c = c + 1                    

    required_string = "✅ Successfully kicked **{}** inactive user's who have not been active for over a month 👋🏼"
    await event.reply(required_string.format(c))



from pyrogram import filters
from pyrogram import enums
from pyrogram.types import *
from ZeroTwo import pgram as bot, DRAGONS as SUDO

async def is_owner(chat_id: int, user_id: int):
    async for x in bot.get_chat_members(chat_id):
        if x.status == enums.ChatMemberStatus.OWNER:
            if x.user.id == user_id or user_id == SUDO:
                return True
            else:
                return False

@bot.on_message(filters.command(["unbanall"]))
async def unbanall(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if (await is_owner(chat_id, user_id)) == False:
        return await message.reply("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("`This Command Only Works in Groups!`")
    else:
        try:
            # Initial message indicating that the search is in progress
            status_message = await message.reply("`Searching participants list...`")

            BANNED = []
            unban = 0
            async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
                # Only process if the banned member is a user
                if m.user:
                    BANNED.append(m.user.id)
                    await bot.unban_chat_member(chat_id, m.user.id)
                    unban += 1

            if unban == 0:
                await status_message.edit("`No one is banned in this chat.`")
            else:
                await status_message.edit(f"**Found Banned Members**: `{len(BANNED)}`\n**Unbanned Successfully**: `{unban}`")

        except Exception as e:
            print(e)

@bot.on_message(filters.command(["unmuteall"]))
async def unmuteall(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if (await is_owner(chat_id, user_id)) == False:
        return await message.reply("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("`This Command Only Works in Groups!`")
    else:
        try:
            # Initial message indicating that the search is in progress
            status_message = await message.reply("`Searching restricted participants list...`")

            RESTRICTED = []
            unrestrict = 0
            async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
                # Only process if the restricted member is a user
                if m.user:
                    RESTRICTED.append(m.user.id)
                    await bot.unban_chat_member(chat_id, m.user.id)  # Unrestrict the user
                    unrestrict += 1

            if unrestrict == 0:
                await status_message.edit("`No one is restricted in this chat.`")
            else:
                await status_message.edit(f"**Found Restricted Members**: `{len(RESTRICTED)}`\n**Unrestricted Successfully**: `{unrestrict}`")

        except Exception as e:
            print(e)
            

__mod_name__ = "𝙼ᴀss𝙰ᴄᴛɪᴏɴs"

__help__ = """
❍ /unbanall: This command allows the group owner to unban all previously banned group members with a single click. Please note that only the owner of the group can use this command.

❍ /unmuteall: With this command, you can unmute all group members at once. It is particularly useful if you have a large group and need to unmute all muted users quickly.

❍ /kickthefools: This command enables the group owner to kick all the inactive members who have been inactive for a month. It is a useful tool to keep the group active and relevant.
 """
