import random
from telethon import events
from ZeroTwo import tbot as neko

GIF = (
    "https://telegra.ph/file/ef94f2f61aa4d9394ef23.mp4",
    "https://telegra.ph/file/b82442bf9ebc32534f7a2.mp4",
    "https://telegra.ph/file/70d43e136125f9c120d2e.mp4",
    "https://telegra.ph/file/45354d3e42982f8de78f4.mp4",
    "https://telegra.ph/file/a22a0930f069686a0c4ef.mp4",
)

@neko.on(events.NewMessage(pattern="/wish ?(.*)$"))
async def wish(e):
    if e.is_reply:
        mm = random.randint(1, 100)
        lol = await e.get_reply_message()
        fire = "https://telegra.ph/file/d6c2cd346255a33b3a023.mp4"
        await neko.send_file(
            e.chat_id,
            fire,
            caption=f"**Hello, {e.sender.first_name}! To make a wish, please use the format /wish (Your Wish) 🙃**",
            reply_to=lol,
        )
    elif e.pattern_match.group(1):
        mm = random.randint(1, 100)
        wish_text = e.pattern_match.group(1)
        fire = random.choice(GIF)
        await neko.send_file(
            e.chat_id,
            fire,
            caption=f"**❄️ Hᴇʏ! {e.sender.first_name}, ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛᴇᴅ\n✨ ʏᴏᴜʀ ᴡɪꜱʜ : {wish_text}\n🫧 ᴘᴏssɪʙɪʟɪᴛɪᴇs : {mm}%**",
            reply_to=e,
        )
    else:
        await neko.send_message(
            e.chat_id,
            "Please tell me your wish by using the format /wish (Your Wish)",
            reply_to=e,
        )
        
