import datetime
import os

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from telethon import events

from pyrogram.types import Message
from pyrogram import filters

from ZeroTwo import dispatcher, tbot, pgram as Luffy, LOGFILE, DEV_USERS
from ZeroTwo.modules.helper_funcs.chat_status import dev_plus

DEBUG_MODE = False


@dev_plus
def debug(update: Update, context: CallbackContext):
    global DEBUG_MODE
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message
    print(DEBUG_MODE)
    if len(args) > 1:
        if args[1] in ("yes", "on"):
            DEBUG_MODE = True
            message.reply_text("Debug mode is now on.")
        elif args[1] in ("no", "off"):
            DEBUG_MODE = False
            message.reply_text("Debug mode is now off.")
    elif DEBUG_MODE:
        message.reply_text("Debug mode is currently on.")
    else:
        message.reply_text("Debug mode is currently off.")


@tbot.on(events.NewMessage(pattern="[/!?.,].*"))
async def i_do_nothing_yes(event):
    global DEBUG_MODE
    if DEBUG_MODE:
        print(f"-{event.from_id} ({event.chat_id}) : {event.text}")
        if os.path.exists("updates.txt"):
            with open("updates.txt", "r") as f:
                text = f.read()
            with open("updates.txt", "w+") as f:
                f.write(f"{text}\n-{event.from_id} ({event.chat_id}) : {event.text}")
        else:
            with open("updates.txt", "w+") as f:
                f.write(
                    f"- {event.from_id} ({event.chat_id}) : {event.text} | {datetime.datetime.now()}"
                )


@Luffy.on_message(filters.command("logs") & filters.user(DEV_USERS))
async def send_log(c: Luffy, m: Message):
    replymsg = await m.reply_text("Sending logs...!")
    # Send logs
    with open(LOGFILE) as f:
        raw = ((f.read()))[1]
    await m.reply_document(
        document=LOGFILE,
        quote=True,
    )
    await replymsg.delete()
    return
    

DEBUG_HANDLER = CommandHandler("debug", debug, run_async=True)
dispatcher.add_handler(DEBUG_HANDLER)

__mod_name__ = "Debug"
__command_list__ = ["debug"]
__handlers__ = [DEBUG_HANDLER]
