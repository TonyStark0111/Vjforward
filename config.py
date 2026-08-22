# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from os import environ 

class Config:
    API_ID = int(environ.get("API_ID", "30547492"))
    API_HASH = environ.get("API_HASH", "a280560d62503a8bdca8642fa9eb26bf")
    BOT_TOKEN = environ.get("BOT_TOKEN", "") 
    BOT_SESSION = environ.get("BOT_SESSION", "vjbot") 
    DATABASE_URI = environ.get("DATABASE_URI", "mongodb+srv://Leechbot1:Leechbot1@cluster0.5cvmpxp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DATABASE_NAME = environ.get("DATABASE_NAME", "testing")
    BOT_OWNER = int(environ.get("BOT_OWNER", "8424998621"))
    LINK_REMOVE_FORWD = environ.get("LINK_REMOVE_FORWD", "True") == "True"


class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
    BOT_SELECTION = {}
    BOT_BUSY = {}
