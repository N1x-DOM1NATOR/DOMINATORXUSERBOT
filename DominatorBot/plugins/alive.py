import datetime
import random
import time

from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from DominatorBot.sql.gvar_sql import gvarstat
from . import *

#-------------------------------------------------------------------------------

ALIVE_TEMP = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┣<b><i>🔥🔥Ꭰօʍìղąէօɾβօէ įʂ ටղƑìɾҽ🔥🔥</b></i>
┣<i><b>-𝕯𝖔𝖒𝖎𝖓𝖆𝖙𝖔𝖗 Աʂҽɾ--</i></b> : 『 <a href='tg://user?id={}'>{}</a> 』
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
╔════✣✤༻⋇༺✤✣════╗
┣─ <b>♦️ ͲҽӀҽէհօղ ┣</b> <i>{}</i>
┣─ <b>♦️ 𝕯𝖔𝖒𝖎𝖓𝖆𝖙𝖔𝖗 ┣</b> <i>{}</i>
┣─ <b>♦️ ʂմժօ ┣</b> <i>{}</i>
┣─ <b>♦️βօէ Աքէìʍҽ ┣</b> <i>{}</i>
┣─ <b>♦️βօէ φìղց ┣</b> <i>{}</i>
╚════✣✤༻⋇༺✤✣════╝
┏━━━━━(φօաҽɾƑմӀӀ=𝕯𝖔𝖒𝖎𝖓𝖆𝖙𝖔𝖗)━━━━━┓
┣─<b><i>💥💥💥 <a href='https://t.me/dominator_bot_official'>[♦️ටղƑìɾҽ-𝕯𝖔𝖒𝖎𝖓𝖆𝖙𝖔𝖗♦️]</a> 💥💥💥</i></b>
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

msg = """{}\n
<b><i>🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅</b></i>
<b>Telethon ≈</b>  <i>{}</i>
<b>Dominatorẞø† ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Abuse ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""
#-------------------------------------------------------------------------------

@dominator_cmd(pattern="alive$")
async def up(event):
    cid = await client_id(event)
    ForGo10God, DOMINATOR_USER, dominator_mention = cid[0], cid[1], cid[2]
    start = datetime.datetime.now()
    dominator = await eor(event, "`Ꭰօʍìղąէօɾβօէ įʂ ටղƑìɾҽ....`")
    uptime = await get_time((time.time() - StartTime))
    a = gvarstat("ALIVE_PIC")
    pic_list = []
    if a:
        b = a.split(" ")
        if len(b) >= 1:
            for c in b:
                pic_list.append(c)
        PIC = random.choice(pic_list)
    else:
        PIC = "https://telegra.ph/file/93f5cc37e28743aeef809.mp4"
    end = datetime.datetime.now()
    ling = (end - start).microseconds / 1000
    omk = ALIVE_TEMP.format(ForGo10God, DOMINATOR_USER, tel_ver, dominator_ver, is_sudo, uptime, ling)
    await event.client.send_file(event.chat_id, file=PIC, caption=omk, parse_mode="HTML")
    await dominator.delete()



@dominator_cmd(pattern="dominator$")
async def dominator_a(event):
    cid = await client_id(event)
    N1xDOMINATOR, DOMINATOR_USER, dominator_mention = cid[0], cid[1], cid[2]
    uptime = await get_time((time.time() - StartTime))
    am = gvarstat("ALIVE_MSG") or "<b>Ꭰօʍìղąէօɾβօէ įʂ ටղƑìɾҽ</b>"
    try:
        dominator = await event.client.inline_query(Config.BOT_USERNAME, "alive")
        await dominator[0].click(event.chat_id)
        if event.sender_id == ForGo10God:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg.format(am, tel_ver, dominator_ver, uptime, abuse_m, is_sudo), parse_mode="HTML")


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "dominator", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "✅ Harmless Module"
).add()
