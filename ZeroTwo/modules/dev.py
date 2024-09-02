import os
from os import environ, execle
import subprocess
import sys
from time import sleep
import asyncio

from telegram import TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler

from pyrogram import filters

from ZeroTwo import dispatcher, DEV_USERS, pgram
from ZeroTwo.modules.helper_funcs.chat_status import dev_plus


@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    if args := context.args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
            update.effective_message.reply_text("Beep boop, I left that soup!.")
        except TelegramError:
            update.effective_message.reply_text(
                "Beep boop, I could not leave that group(dunno why tho)."
            )
    else:
        update.effective_message.reply_text("Send a valid chat ID")
        

@pgram.on_message(filters.command("misapull") & filters.user(DEV_USERS))
async def git_pull_command(client, message):
    try:
        result = subprocess.run(
            ["git", "pull", "https://gittoken@github.com/Shinigamiiz/ZeroTwo.git", "Makima"],
            capture_output=True, text=True, check=True
        )
        if "Already up to date" in result.stdout:
            return await message.reply("Repo is already up to date")
        elif result.returncode == 0:
            await message.reply(f"Git pull successful. Bot updated.\n\n`{result.stdout}`")
            await restart_bot(message)
        else:
            await message.reply("Git pull failed. Please check the logs.")
    except subprocess.CalledProcessError as e:
        await message.reply(f"Git pull failed with error: {e.stderr}")

async def restart_bot(message):
    await message.reply("`Restarting... 🤯🤯`")
    args = [sys.executable, "-m", "ZeroTwo"] # Adjust this line as needed
    os.execle(sys.executable, *args, os.environ)
    sys.exit()
    

@pgram.on_message(filters.command("restart") & filters.user(DEV_USERS))
async def restart_command(client, message):
    try:
        await message.reply("Restarting the bot...")
        os.execvp(sys.executable, [sys.executable, "-m", "ZeroTwo"])
    except Exception as e:
        await message.reply(f"Restart failed with error: {str(e)}")


LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)

dispatcher.add_handler(LEAVE_HANDLER)

__mod_name__ = "Dev"
__handlers__ = [LEAVE_HANDLER]

