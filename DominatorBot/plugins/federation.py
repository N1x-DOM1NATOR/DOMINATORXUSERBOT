import asyncio
import os
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon import functions, types, events
from . import *

logs_id = Config.FBAN_LOG_GROUP
fbot = "@MissRose_bot"


@dominator_cmd(pattern="newfed ([\s\S]*)")
async def _(event):
    dominator_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    dominator = await eor(event, "`Making new fed...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=609517172)
            )
            await event.client.send_message(chat, f"/newfed {dominator_input}")
            response = await response
        except YouBlockedUserError:
            await eod(dominator, "`Please unblock` @MissRose_Bot `and try again`")
            return
        if response.text.startswith("You already have a federation"):
            await eod(dominator, f"You already have a federation. Do {hl}renamefed to rename your current fed.")
        else:
            await dominator.edit(f"{response.message.message}")


@dominator_cmd(pattern="renamefed ([\s\S]*)")
async def _(event):
    dominator_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    dominator = await eor(event, "`Trying to rename your fed...`")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=609517172))
              await event.client.send_message(chat, f"/renamefed {dominator_input}")
              response = await response 
          except YouBlockedUserError: 
              await eod(dominator, "Please Unblock @MissRose_Bot")
              return
          else:
             await dominator.edit(response.message)


@dominator_cmd(pattern="fstat ([\s\S]*)")
async def _(event):
    dominator = await eor(event, "`Collecting fstat....`")
    thumb = dominator_logo
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        lavde = str(previous_message.sender_id)
        user = f"[user](tg://user?id={lavde})"
    else:
        lavde = event.pattern_match.group(1)
        user = lavde
    if lavde == "":
        await dominator.edit("`Need username/id to check fstat`")
        return
    else:
        async with event.client.conversation(fbot) as conv:
            try:
                await conv.send_message("/fedstat " + lavde)
                await asyncio.sleep(4)
                response = await conv.get_response()
                await asyncio.sleep(2)
                await event.client.send_message(event.chat_id, response)
                await event.delete()
            except YouBlockedUserError:
                await dominator.edit("`Please Unblock` @MissRose_Bot")


@dominator_cmd(pattern="fedinfo ([\s\S]*)")
async def _(event):
    dominator = await eor(event, "`Fetching fed info.... please wait`")
    lavde = event.pattern_match.group(1)
    async with event.client.conversation(fbot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + lavde)
            massive = await conv.get_response()
            await dominator.edit(massive.text + "\n\n**ʟɛɢɛռɖaʀʏ_ᴀғ_ɦɛʟʟɮօt**")
        except YouBlockedUserError:
            await dominator.edit("`Please Unblock` @MissRose_Bot")
            
            
CmdHelp("federation").add_command(
  "newfed", "<newfed name>", "Makes a federation of Rose bot"
).add_command(
  "renamefed", "<new name>", "Renames the fed of Rose Bot"
).add_command(
  "fstat", "<username/id>", "Gets the fban stats of the user from rose bot federation"
).add_command(
  "fedinfo", "<fed id>", "Gives details of the given fed id"
).add_info(
  "Rose Bot Federation."
).add_warning(
  "✅ Harmless Module."
).add()
