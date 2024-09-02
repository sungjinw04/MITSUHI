from functools import wraps

from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.types import Message, CallbackQuery

from ZeroTwo import DRAGONS
from ZeroTwo import pgram


async def authorised(func, subFunc2, client, message, *args, **kwargs):
    chatID = message.chat.id if isinstance(message, Message) else message.message.chat.id
    try:
        await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
        await pgram.leave_chat(chatID)
    except Exception as e:
        if isinstance(message, Message):
            try:
                await message.reply_text(str(e))
            except ChatWriteForbidden:
                await pgram.leave_chat(chatID)
        elif isinstance(message, CallbackQuery):
            try:
                await message.answer(str(e))
            except ChatWriteForbidden:
                await pgram.leave_chat(chatID)
    return subFunc2


async def unauthorised(message: Message, permission, subFunc2):
    chatID = message.chat.id if isinstance(message, Message) else message.message.chat.id
    text = (
        "You don't have the required permission to perform this action."
        + f"\n**Permission:** __{permission}__"
    )
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await pgram.leave_chat(chatID)
    return subFunc2


def adminsOnly(permission):
    def subFunc(func):
        @wraps(func)
        async def subFunc2(client, message, *args, **kwargs):
            chatID = message.chat.id if isinstance(message, Message) else message.message.chat.id
            if not message.from_user:
                # For anonymous admins
                if message.sender_chat:
                    return await authorised(
                        func, subFunc2, client, message, *args, **kwargs
                    )
                return await unauthorised(message, permission, subFunc2)
            # For admins and sudo users
            userID = message.from_user.id
            permissions = await member_permissions(chatID, userID)
            if userID not in DRAGONS and permission not in permissions:
                return await unauthorised(message, permission, subFunc2)
            return await authorised(
                func, subFunc2, client, message, *args, **kwargs
            )

        return subFunc2

    return subFunc


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = (await pgram.get_chat_member(chat_id, user_id)).privileges
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_video_chats:
        perms.append("can_manage_video_chats")
    return perms

