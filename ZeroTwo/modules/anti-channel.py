import html

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.filters import Filters

from pyrogram import Client, filters, enums
from pyrogram.raw import types, functions

from ZeroTwo import pgram
from ZeroTwo.modules.helper_funcs.anonymous import AdminPerms, user_admin
from ZeroTwo.modules.helper_funcs.decorators import nekocmd as Himawaricmd, nekomsg as Himawarimsg
from ZeroTwo.modules.sql.antichannel_sql import (
    antichannel_status,
    disable_antichannel,
    enable_antichannel,
)


@Himawaricmd(command="antichannel", group=100)
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html(f"Enabled Antichannel in {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html(f"Disabled Antichannel in {html.escape(chat.title)}")
        else:
            message.reply_text(f"Unrecognized arguments {s}")
        return
    message.reply_html(
        f"Antichannel setting is currently {antichannel_status(chat.id)} in {html.escape(chat.title)}"
    )

@pgram.on_message(filters.group,group=23)
async def _message_handler(client, message):
    chat_id = message.chat.id
    if not (antichannel_status(message.chat.id)):
        return
    if message.sender_chat and message.sender_chat.type == enums.ChatType.CHANNEL and not message.chat.linked_chat:
        try:
            await message.delete()
            channel_id = message.sender_chat.id
            await client.invoke(functions.channels.EditBanned(
                    channel=await client.resolve_peer(chat_id),
                    participant=await client.resolve_peer(channel_id),
                    banned_rights=types.ChatBannedRights(
                        until_date=0,
                        view_messages=True,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_polls=True)))

            channel_username = message.sender_chat.username if message.sender_chat.username else "This channel"
            notification_msg = f"**@{channel_username} channel profile has been removed.**"
            await client.send_message(chat_id, notification_msg)
        except Exception as e:
            print(e)
                    

__mod_name__ = "𝙰ɴᴛɪ-𝙲ʜᴀɴɴᴇʟ"

__help__ = """
Anti Channel Mode is a mode to automatically ban users who chat using Channels.
This command can only be used by Admins.

/antichannel <'on'/'yes'> : enables anti-channel
/antichannel <'off'/'no'> : disabled anti-channel
"""
