import logging
import os
import sys
import datetime
import time
import httpx
import pyromod
from sys import stdout
import pymongo
import spamwatch
import aiohttp
import telegram.ext as tg
from motor import motor_asyncio
from pyromod import listen
from redis import StrictRedis
from Python_ARQ import ARQ
from httpx import AsyncClient, Timeout
from pymongo import MongoClient
from odmantic import AIOEngine
from pyrogram import Client, errors
from telethon.sessions import StringSession
from telethon import TelegramClient
from aiohttp import ClientSession

StartTime = time.time()

LOG_DATETIME = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
LOGDIR = f"{__name__}/logs"

# Make Logs directory if it does not exixts
if not os.path.isdir(LOGDIR):
    os.mkdir(LOGDIR)

LOGFILE = f"{LOGDIR}/{__name__}_{LOG_DATETIME}_log.txt"

file_handler = logging.FileHandler(filename=LOGFILE)
stdout_handler = logging.StreamHandler(stdout)

logging.basicConfig(
    format="%(asctime)s - [ZeroTwo] - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[file_handler, stdout_handler],
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

log = logging.getLogger('[Your Bot Is Building]')

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.]"
    )
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get('INFOPIC', False))
    EVENT_LOGS = os.environ.get('EVENT_LOGS', None)
    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    ARQ_API_URL = os.environ.get("ARQ_API_URL", None)
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get('API_ID', None)
    API_HASH = os.environ.get('API_HASH', None)
    DB_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER',
                                 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    CMD_OP = int(os.environ.get("CMD_OP", "/ . ? !").split())
    CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
    TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
    AI_API_KEY = os.environ.get('AI_API_KEY', None)
    WALL_API = os.environ.get('WALL_API', None)
    SUPPORT_CHAT = os.environ.get('SUPPORT_CHAT', None)
    REPOSITORY = os.environ.get("REPOSITORY", "")
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    TELEGRAPH_SHORT_NAME = os.environ.get("TELEGRAPH_SHORT_NAME", "lightYagami")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    BOT_NAME = os.environ.get("BOT_NAME", True) # Name Of your Bot.4
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "") # Bot Username
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "") # From:- https://openweathermap.org/api
    LOG_GROUP_ID = os.environ.get('LOG_GROUP_ID', None)
    HELP_IMG = os.environ.get("HELP_IMG", True)
    MONGO_DB = "Shikimori"
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    ERROR_LOGS = os.environ.get("ERROR_LOGS", None) # Error Logs (Channel Ya Group Choice Is Yours) (-100)
    DEBUG = bool(os.environ.get('IS_DEBUG', False))
    REDIS_URL = os.environ.get("REDIS_URL", None) # REDIS URL (From:- Heraku & Redis)
    OWNER_NAME = os.environ.get("OWNER_NAME", None)

    try:
        BL_CHATS = set(int(x) for x in os.environ.get('BL_CHATS', "").split())
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")
    
else:
    from ZeroTwo.config import Development as Config
    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH

    DB_URI = Config.DB_URI
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    HELP_IMG = Config.HELP_IMG
    DEL_CMDS = Config.DEL_CMDS
    MONGO_DB = Config.MONGO_DB
    MONGO_DB_URI = Config.MONGO_DB_URI
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    OWNER_NAME = Config.OWNER_NAME
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    INFOPIC = Config.INFOPIC
    ARQ_API_URL = Config.ARQ_API_URL
    ARQ_API_KEY = Config.ARQ_API_KEY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    ERROR_LOGS = Config.ERROR_LOGS

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(5667156680)

session_name = TOKEN.split(":")[0]
pgram = Client(session_name, api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

STRICT_GMUTE = "yes"
mongodb = MongoClient(MONGO_DB_URI, 27017)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)

#install aiohttp session
print("Scanning AIO http session")
aiohttpsession = ClientSession() 

#install arq
print("Connecting ARQ Client")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
tbot = TelegramClient("ZeroTwo", API_ID, API_HASH)
pbot = Client("ZeroTwo", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
dispatcher = updater.dispatcher

BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

timeout = httpx.Timeout(40)
http = httpx.AsyncClient(http2=True, timeout=timeout)


DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from ZeroTwo.modules.helper_funcs.handlers import (CustomCommandHandler,
                                                        CustomMessageHandler,
                                                        CustomRegexHandler)
                                                        

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

print("Connecting Pyrogram Client")

print("Checking Errors")

REDIS_URL = "redis://default:6vsajwd6wq3lNI7T3zMIpltTrU040DJC@redis-19248.c16.us-east-1-3.ec2.cloud.redislabs.com:19248"


REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("Connecting To Redis Database")

except BaseException:

    raise Exception("[ERROR]: Your Redis Database Is Not Alive, Please Check Again.")

finally:

   REDIS.ping()
