from DominatorBot import *
from DominatorBot.clients.session import bot, tgbot

from ..config import Config
from .decorators import *

USER = bot.me.first_name
USER_ID = bot.uid
mention = f"[{USER}](tg://user?id={USER_ID})"
