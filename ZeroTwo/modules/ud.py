import requests
from ZeroTwo.events import register
from telethon import Button
from telegram.error import BadRequest

@register(pattern="[/!]ud")
async def ud_(e):
    try:
        text = e.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await e.reply("Please enter keywords to search on ud!")

    url = f"https://api.urbandictionary.com/v0/define?term={text}"
    response = requests.get(url)
    results = response.json()

    if results.get("list"):
        definition = results["list"][0].get("definition", "")
        example = results["list"][0].get("example", "")
        definition = definition.replace("[", "").replace("]", "")
        example = example.replace("[", "").replace("]", "")

        reply_txt = f'Word: {text}\n\nDefinition:\n{definition}\n\nExample:\n{example}'
    else:
        reply_txt = f'Word: {text}\n\nResults: Sorry, could not find any matching results!'

    google_search_url = f"https://www.google.com/search?q={text}"
    await e.reply(reply_txt, buttons=Button.url("🔎 Google it!", google_search_url), parse_mode="html")


__help__ = """
 ❍ /ud <Word you want to search for>*:* get the dictionary of given query.
"""

__mod_name__ = "𝙳ɪᴄᴛɪᴏɴᴀʀʏ"
