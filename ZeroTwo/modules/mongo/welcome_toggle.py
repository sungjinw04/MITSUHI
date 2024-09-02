from ZeroTwo import db

dwelcomedb = db.dwelcome

async def is_dwelcome_on(chat_id: int) -> bool:
    chat = await dwelcomedb.find_one({"chat_id_toggle": chat_id})
    return not bool(chat)


async def dwelcome_on(chat_id: int):
    await dwelcomedb.delete_one({"chat_id_toggle": chat_id})


async def dwelcome_off(chat_id: int):
    await dwelcomedb.insert_one({"chat_id_toggle": chat_id})
  
