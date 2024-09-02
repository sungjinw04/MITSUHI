import os
import subprocess
from datetime import datetime, timedelta
import asyncio
from pyrogram import (
    filters,
    Client
)

from ZeroTwo import pgram as app

OWNER_ID = 2033411815
POSTGRESQL_URL = 'postgresql://levi:levi@localhost/levibotttt'
backup_file = f"/Makima.sql"

def backup_process():
    try:
        backup_command = f"pg_dump '{POSTGRESQL_URL}' > {backup_file}"
        subprocess.run(backup_command, shell=True, check=True)
        return True
    except:
        return False

@app.on_message(filters.command("backup") & filters.private)
async def backup_handler(client, msg):
    user_id = msg.from_user.id
    if user_id != OWNER_ID:
        return

    result = backup_process()
    if result == True:
        await msg.reply_text("Backup Created successfully!!")
        with open(backup_file, "rb") as file:
            await msg.reply_document(file)

    else:
        await msg.reply_text("Something went wrong while creating the backup!!")
        
