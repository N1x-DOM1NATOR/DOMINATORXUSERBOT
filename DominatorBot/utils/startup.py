import os
import glob
from pathlib import Path

from telethon import Button
from telethon.tl import functions
from telethon.tl.types import ChatAdminRights

from DominatorBot import LOGS, bot
from DominatorBot.config import Config
from DominatorBot.helpers.int_str import make_int
from DominatorBot.sql.gvar_sql import addgvar, gvarstat
from . import load_module

BOTLOG_CHATID = Config.LOGGER_ID

# Creates the logger group on first deploy and adds the helper bot
async def logger_id(client):
    desc = "A Bot Logger Group For DominatorBot. DO NOT LEAVE THIS GROUP!!"
    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    try:
        grp = await client(functions.channels.CreateChannelRequest(title="DominatorBot Logger", about=desc, megagroup=True))
        grp_id = grp.chats[0].id
        grp = await client(functions.messages.ExportChatInviteRequest(peer=grp_id))
        await client(functions.channels.InviteToChannelRequest(channel=grp_id, users=[Config.BOT_USERNAME]))
        await client(functions.channels.EditAdminRequest(grp_id, Config.BOT_USERNAME, new_rights, "Helper"))
    except Exception as e:
        LOGS.error(f"{str(e)}")
    if not str(grp_id).startswith("-100"):
        grp_id = int("-100" + str(grp_id))
    return grp_id


# Updates sudo cache on every restart
async def update_sudo():
    Sudo = Config.SUDO_USERS
    sudo = gvarstat("SUDO_USERS")
    if sudo:
        int_list = await make_int(gvarstat("SUDO_USERS"))
        for x in int_list:
            Sudo.append(x)


# Checks for logger group.
async def logger_check(bot):
    if Config.LOGGER_ID is None:
        if gvarstat("LOGGER_ID") is None:
            grp_id = await logger_id(bot)
            addgvar("LOGGER_ID", grp_id)
            Config.LOGGER_ID = grp_id
        Config.LOGGER_ID = int(gvarstat("LOGGER_ID"))


# Sends the startup message to logger group
async def start_msg(client, pic, version, total):
    is_sudo = "True" if Config.SUDO_USERS else "False"
    text = f"""
#START

<b><i>Version :</b></i> <code>{version}</code>
<b><i>Clients :</b></i> <code>{str(total)}</code>
<b><i>Sudo :</b></i> <code>{is_sudo}</code>

<b><i>»» <u><a href='https://t.me/dominator_bot_official'>💥Dominatorβօէ💥</a></u> ««</i></b>
"""
    await client.send_file(
        Config.LOGGER_ID,
        pic,
        caption=text,
        parse_mode="HTML",
        buttons=[[Button.url("💥Dominatorβօէ💥", "https://t.me/dominator_bot_official")]],
    )


# Joins the DominatorBot chat and channel from all clients
async def join_it(client):
    if client:
        try:
            await client(functions.channels.JoinChannelRequest("@dominator_bot_official"))
            await client(functions.channels.JoinChannelRequest("@dominator_bot_official"))
        except BaseException:
            pass


async def load_plugins(folder, extfolder=None):
    """
    To load plugins from the mentioned folder
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"DominatorBot/{folder}/*.py"
        plugin_path = f"DominatorBot/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.UNLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname.replace(".py","")
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"unable to load {shortname} because of error {e}\nBase Folder {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await bot.send_message(
            BOTLOG_CHATID,
            f'Your external repo plugins have imported \n**No of imported plugins :** `{success}`\n**Failed plugins to import :** `{", ".join(failure)}`')

# DominatorBot
