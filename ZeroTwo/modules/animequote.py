import json
import requests
import random

from ZeroTwo import dispatcher
from ZeroTwo.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async, CallbackQueryHandler
from telegram import ParseMode, Update, InlineKeyboardMarkup, InlineKeyboardButton, replymarkup, ChatPermissions

def anime_quote():
    quotes = [
        ("Believe in yourself. Not in the you who believes in me. Not the me who believes in you. Believe in the you who believes in yourself.", "Kamina", "Tengen Toppa Gurren Lagann"),
        ("It's not the face that makes someone a monster, it's the choices they make with their lives.", "Naruto Uzumaki", "Naruto"),
        ("The only thing that can defeat power is more power. That is the one constant in this universe. However, there is no point in power if it consumes itself.", "Itachi Uchiha", "Naruto"),
        ("No one knows what the future holds. That's why its potential is infinite.", "Rintarou Okabe", "Steins;Gate"),
        ("Don't forget. Always, somewhere, someone is fighting for you. As long as you remember her, you are not alone.", "Madoka Kaname", "Puella Magi Madoka Magica"),
        ("The only thing we're allowed to do is to believe that we won't regret the choice we made.", "Levi Ackerman", "Attack on Titan"),
        ("Whatever you do, enjoy it to the fullest. That is the secret of life.", "Rider (Iskandar)", "Fate/Zero"),
        ("If you don't take risks, you can't create a future.", "Monkey D. Luffy", "One Piece"),
        ("In order to grow, you must face the pain of the past. Accept it and move forward.", "Erza Scarlet", "Fairy Tail"),
        ("Sometimes the things that matter the most are right in front of you.", "Asuna Yuuki", "Sword Art Online"),
        ("The world’s not perfect, but it’s there for us trying the best it can. That’s what makes it so damn beautiful.", "Roy Mustang", "Fullmetal Alchemist: Brotherhood"),
        ("If nobody cares to accept you and wants you in this world, accept yourself and you will see that you don’t need them and their selfish ideas.", "Gintoki Sakata", "Gintama"),
        ("Whatever you do, you should do it with all your heart.", "Saber (Artoria Pendragon)", "Fate/stay night: Unlimited Blade Works"),
        ("Even if things are painful and tough, people should appreciate what it means to be alive at all.", "Yato", "Noragami"),
        ("I'd rather die on my feet than live on my knees.", "Eren Yeager", "Attack on Titan"),
        # Add 15 new quotes here
        ("I don't want to conquer anything. I just think the guy with the most freedom in this whole ocean... is the Pirate King!", "Monkey D. Luffy", "One Piece"),
        ("It's not the strength of a hero that matters, but the strength of their heart.", "Natsu Dragneel", "Fairy Tail"),
        ("The world is merciless, and it's also very beautiful.", "Mikasa Ackerman", "Attack on Titan"),
        ("No one knows what the future holds. That's why we can never say goodbye.", "Isaac Netero", "Hunter x Hunter"),
        ("If you wanna make people dream, you've gotta start by believing in that dream yourself!", "Shoyo Hinata", "Haikyuu!!"),
        ("Being weak is nothing to be ashamed of. Staying weak is.", "Izuku Midoriya", "My Hero Academia"),
        ("Even if you’re weak, there are miracles you can seize with your hands if you fight on to the very end.", "Gon Freecss", "Hunter x Hunter"),
        ("There are no shortcuts in life. To win, you have to work hard, face your demons, and never give up.", "Yami Sukehiro", "Black Clover"),
        ("True strength comes from the heart, not just brute force.", "Edward Elric", "Fullmetal Alchemist"),
        ("The fear of death follows from the fear of life. A man who lives fully is prepared to die at any time.", "Shinobu Sensui", "Yu Yu Hakusho"),
        ("In this world, wherever there is light – there are also shadows. As long as the concept of winners exists, there must also be losers.", "Lelouch vi Britannia", "Code Geass"),
        ("I’d rather trust and regret than doubt and regret.", "Kiritsugu Emiya", "Fate/Zero"),
        ("You should never give up on life, no matter how you feel. No matter how hard things get, you have to hold on to your life, no matter what.", "Misaki Takahashi", "Junjou Romantica"),
        ("The true measure of a shinobi is not how he lives but how he dies. It's not what they do in life, but what they did before dying that proves their worth.", "Jiraiya", "Naruto"),
    ]
    quote, character, anime = random.choice(quotes)
    return quote, character, anime
    
def quotes(update: Update, context: CallbackContext):
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝ {quote}❞</i>\n\n<b>{character}</b> from <b>{anime}</b>"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Change 🔁",
            callback_data="change_quote")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )
    
def change_quote(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝ {quote}❞</i>\n\n<b>{character}</b> from <b>{anime}</b>"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Change 🔁",
            callback_data="quote_change")]])
    message.edit_text(msg, reply_markup=keyboard,
                      parse_mode=ParseMode.HTML)
    
def animequotes(update: Update, context: CallbackContext):
    message = update.effective_message
    name = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name
    keyboard = [[InlineKeyboardButton(text="Change", callback_data="changek_quote")]]
    message.reply_photo(random.choice(QUOTES_IMG),reply_markup=InlineKeyboardMarkup(keyboard))

def changek_quote(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    keyboard = [[InlineKeyboardButton(text="Change", callback_data="quotek_change")]]
    message.reply_photo(random.choice(QUOTES_IMG),reply_markup=InlineKeyboardMarkup(keyboard))


QUOTES_IMG = (
      "https://i.imgur.com/Iub4RYj.jpg", 
      "https://i.imgur.com/uvNMdIl.jpg", 
      "https://i.imgur.com/YOBOntg.jpg", 
      "https://i.imgur.com/fFpO2ZQ.jpg", 
      "https://i.imgur.com/f0xZceK.jpg", 
      "https://i.imgur.com/RlVcCip.jpg", 
      "https://i.imgur.com/CjpqLRF.jpg", 
      "https://i.imgur.com/8BHZDk6.jpg", 
      "https://i.imgur.com/8bHeMgy.jpg", 
      "https://i.imgur.com/5K3lMvr.jpg", 
      "https://i.imgur.com/NTzw4RN.jpg", 
      "https://i.imgur.com/wJxryAn.jpg", 
      "https://i.imgur.com/9L0DWzC.jpg", 
      "https://i.imgur.com/sBe8TTs.jpg", 
      "https://i.imgur.com/1Au8gdf.jpg", 
      "https://i.imgur.com/28hFQeU.jpg", 
      "https://i.imgur.com/Qvc03JY.jpg", 
      "https://i.imgur.com/gSX6Xlf.jpg", 
      "https://i.imgur.com/iP26Hwa.jpg", 
      "https://i.imgur.com/uSsJoX8.jpg", 
      "https://i.imgur.com/OvX3oHB.jpg", 
      "https://i.imgur.com/JMWuksm.jpg", 
      "https://i.imgur.com/lhM3fib.jpg", 
      "https://i.imgur.com/64IYKkw.jpg", 
      "https://i.imgur.com/nMbyA3J.jpg", 
      "https://i.imgur.com/7KFQhY3.jpg", 
      "https://i.imgur.com/mlKb7zt.jpg", 
      "https://i.imgur.com/JCQGJVw.jpg", 
      "https://i.imgur.com/hSFYDEz.jpg", 
      "https://i.imgur.com/PQRjAgl.jpg", 
      "https://i.imgur.com/ot9624U.jpg", 
      "https://i.imgur.com/iXmqN9y.jpg", 
      "https://i.imgur.com/RhNBeGr.jpg", 
      "https://i.imgur.com/tcMVNa8.jpg", 
      "https://i.imgur.com/LrVg810.jpg", 
      "https://i.imgur.com/TcWfQlz.jpg", 
      "https://i.imgur.com/muAUdvJ.jpg", 
      "https://i.imgur.com/AtC7ZRV.jpg", 
      "https://i.imgur.com/sCObQCQ.jpg", 
      "https://i.imgur.com/AJFDI1r.jpg", 
      "https://i.imgur.com/TCgmRrH.jpg", 
      "https://i.imgur.com/LMdmhJU.jpg", 
      "https://i.imgur.com/eyyax0N.jpg", 
      "https://i.imgur.com/YtYxV66.jpg", 
      "https://i.imgur.com/292w4ye.jpg", 
      "https://i.imgur.com/6Fm1vdw.jpg", 
      "https://i.imgur.com/2vnBOZd.jpg", 
      "https://i.imgur.com/j5hI9Eb.jpg", 
      "https://i.imgur.com/cAv7pJB.jpg", 
      "https://i.imgur.com/jvI7Vil.jpg", 
      "https://i.imgur.com/fANpjsg.jpg", 
      "https://i.imgur.com/5o1SJyo.jpg", 
      "https://i.imgur.com/dSVxmh8.jpg", 
      "https://i.imgur.com/02dXlAD.jpg", 
      "https://i.imgur.com/htvIoGY.jpg", 
      "https://i.imgur.com/hy6BXOj.jpg", 
      "https://i.imgur.com/OuwzNYu.jpg", 
      "https://i.imgur.com/L8vwvc2.jpg", 
      "https://i.imgur.com/3VMVF9y.jpg", 
      "https://i.imgur.com/yzjq2n2.jpg", 
      "https://i.imgur.com/0qK7TAN.jpg", 
      "https://i.imgur.com/zvcxSOX.jpg", 
      "https://i.imgur.com/FO7bApW.jpg", 
      "https://i.imgur.com/KK06gwg.jpg", 
      "https://i.imgur.com/6lG4tsO.jpg"
      
      )    


ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("animequotes", animequotes, run_async=True)
QUOTES_HANDLER = DisableAbleCommandHandler("quote", quotes, run_async=True)

CHANGE_QUOTE = CallbackQueryHandler(
    change_quote, pattern=r"change_.*")
QUOTE_CHANGE = CallbackQueryHandler(
    change_quote, pattern=r"quote_.*")
CHANGEK_QUOTE = CallbackQueryHandler(
    changek_quote, pattern=r"changek_.*")
QUOTEK_CHANGE = CallbackQueryHandler(
    changek_quote, pattern=r"quotek_.*")

dispatcher.add_handler(CHANGE_QUOTE)
dispatcher.add_handler(QUOTE_CHANGE)
dispatcher.add_handler(CHANGEK_QUOTE)
dispatcher.add_handler(QUOTEK_CHANGE)
dispatcher.add_handler(ANIMEQUOTES_HANDLER)
dispatcher.add_handler(QUOTES_HANDLER)

__command_list__ = [

    "animequotes",
    "quote"

]

__handlers__ = [

    ANIMEQUOTES_HANDLER,
    QUOTES_HANDLER

]

__help__ = """

Get amazing anime quotes by this module

*Commands:*

• /animequotes*:* Get quotes in picture

• /quote*:* Get text quotes

"""

__mod_name__ = "𝙰ɴɪᴍᴇ 𝚀ᴏᴜᴛᴇs"
