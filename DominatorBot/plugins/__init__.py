import datetime
import time

from DominatorBot import *
from DominatorBot.clients import *
from DominatorBot.config import Config
from DominatorBot.helpers import *
from DominatorBot.utils import *
from DominatorBot.random_strings import *
from DominatorBot.version import __dominator__
from DominatorBot.sql.gvar_sql import gvarstat
from telethon import version

dominator_logo = "./DominatorBot/resources/pics/DominatorBot_logo.jpg"
cjb = "./DominatorBot/resources/pics/cjb.jpg"
restlo = "./DominatorBot/resources/pics/rest.jpeg"
shuru = "./DominatorBot/resources/pics/shuru.jpg"
shhh = "./DominatorBot/resources/pics/chup_madarchod.jpeg"
hl = Config.HANDLER
shl = Config.SUDO_HANDLER
dominator_ver = __dominator__
tel_ver = version.__version__

async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await bot.get_entity(ids)).id
    return userid

is_sudo = "True" if gvarstat("SUDO_USERS") else "False"

abus = Config.ABUSE
if abus == "ON":
    abuse_m = "Enabled"
else:
    abuse_m ="Disabled"


my_channel = Config.MY_CHANNEL or "@dominator_bot_official"
my_group = Config.MY_GROUP or "@dominator_bot_support"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/dominator_bot_official"
dominator_channel = f"[✨Ꭰօʍìղąէօɾβօէ✨]({chnl_link})"
grp_link = "https://t.me/dominator_bot_support"
dominator_grp = f"[✨Ꭰօʍìղąէօɾβօէ Ɠɾօմք✨]({grp_link})"

WELCOME_FORMAT = """**Use these fomats in your welcome note to make them attractive.**
  {mention} :  To mention the user
  {title} : To get chat name in message
  {count} : To get group members
  {first} : To use user first name
  {last} : To use user last name
  {fullname} : To use user full name
  {userid} : To use userid
  {username} : To use user username
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
"""
# will add more soon

# DominatorBot
