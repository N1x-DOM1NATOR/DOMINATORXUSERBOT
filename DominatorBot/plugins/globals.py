import asyncio
import random

from telethon import events
from telethon.tl.types import ChatAdminRights, ChannelParticipantsAdmins, ChatBannedRights, MessageEntityMentionName, MessageMediaPhoto
from telethon.errors.rpcerrorlist import UserIdInvalidError, MessageTooLongError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest

from DominatorBot.sql.gban_sql import is_gbanned, gbaner, ungbaner, all_gbanned
from DominatorBot.sql.gvar_sql import gvarstat
from DominatorBot.sql import gmute_sql as gsql
from . import *


async def get_full_user(event):  
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, "Need a user to do this...")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, f"**ERROR !!**\n\n`{str(err)}`")           
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj



@dominator_cmd(pattern="gpro(?:\s|$)([\s\S]*)")
async def _(event):
    i = 0
    sender = await event.get_sender()
    me = await event.client.get_me()
    dominator = await eor(event, "`Promoting globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await event.get_chat()
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
       k = await dominator.edit("You can't promote yourself...")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await dominator.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await event.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=False,
                               invite_users=True,
                                change_info=False,
                                 ban_users=True,
                                  delete_messages=True,
                                   pin_messages=True)
        for x in telchanel:
          try:
             await event.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await dominator.edit(f"**Promoting User in :**  `{i}` Chats...")
          except:
             pass
    else:
        await dominator.edit(f"**Reply to a user !!**")
    await dominator.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Promoted Globally In** `{i}` **Chats !!**"
    )
    await event.client.send_message(Config.LOGGER_ID, f"#GPROMOTE \n\n**Globally Promoted User :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")


@dominator_cmd(pattern="gdem(?:\s|$)([\s\S]*)")
async def _(event):
    i = 0
    sender = await event.get_sender()
    me = await event.client.get_me()
    dominator = await eor(event, "`Demoting Globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await event.get_chat()
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
       k = await dominator.edit("You can't Demote yourself !!")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await dominator.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await event.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=None,
                               invite_users=None,
                                change_info=None,
                                 ban_users=None,
                                  delete_messages=None,
                                   pin_messages=None)
        for x in telchanel:
          try:
             await event.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await dominator.edit(f"**Demoting Globally In Chats :** `{i}`")
          except:
             pass
    else:
        await dominator.edit(f"**Reply to a user !!**")
    await dominator.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Demoted Globally In** `{i}` **Chats !!**"
    )
    await event.client.send_message(Config.LOGGER_ID, f"#GDEMOTE \n\n**Globally Demoted :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")


@dominator_cmd(pattern="gban(?:\s|$)([\s\S]*)")
async def _(event):
    dominator = await eor(event, f"`Gbanning ...`")
    reason = ""
    cid = await client_id(event)
    ForGo10God, DOMINATOR_USER, dominator_mention = cid[0], cid[1], cid[2]
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await eod(dominator, "**To gban a user i need a userid or reply to his/her message!!**")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(dominator, "🥴 **Nashe me hai kya lawde ‽**")
    if str(userid) in DEVLIST:
        return await eod(dominator, "😑 **GBan my creator ?¿ Really‽**")
    if is_gbanned(userid):
        return await eod(
            dominator,
            "This kid is already gbanned and added to my **Gban Watch!!**",
        )
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(gfuck.id, userid, view_messages=False)
                chats +=1
            except BaseException:
                pass

    gbaner(userid)
    a = gvarstat("BAN_PIC")
    pic_str = []
    if a:
        b = a.split(" ")
        for c in b:
            pic_str.append(c)
        gbpic = random.choice(pic_str)
    else:
        gbpic = cjb
    gmsg = f"🥴 [{name}](tg://user?id={userid}) **beta majdur ko khodna 😪 aur** {dominator_mention} **ko chodna... Kabhi sikhana nhi!! 😏**\n\n📍 Added to Gban Watch!!\n**🔰 Total Chats :**  `{chats}`"
    if reason != "":
        gmsg += f"\n**🔰 Reason :**  `{reason}`"
    ogmsg = f"[{name}](tg://user?id={userid}) **Is now GBanned by** {dominator_mention} **in**  `{chats}`  **Chats!! 😏**\n\n**📍 Also Added to Gban Watch!!**"
    if reason != "":
        ogmsg += f"\n**🔰 Reason :**  `{reason}`"
    if Config.ABUSE == "ON":
        await event.client.send_file(event.chat_id, gbpic, caption=gmsg)
        await dominator.delete()
    else:
        await dominator.edit(ogmsg)


@dominator_cmd(pattern="ungban(?:\s|$)([\s\S]*)")
async def _(event):
    cid = await client_id(event)
    ForGo10God, DOMINATOR_USER, dominator_mention = cid[0], cid[1], cid[2]
    dominator = await eor(event, "`Ungban in progress...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(dominator, "`Reply to a user or give their userid... `")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if not is_gbanned(userid):
        return await eod(dominator, "`User is not gbanned.`")
    await dominator.edit(f"Ungbaning in client 1... \n**Unbanned in :** `{chats}`")
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(gfuck.id, userid, view_messages=True)
                chats += 1
            except BaseException:
                pass

    ungbaner(userid)
    await dominator.edit(
        f"📍 [{name}](tg://user?id={userid}) **is now Ungbanned from `{chats}` chats and removed from Gban Watch!!**",
    )


@dominator_cmd(pattern="listgban$")
async def already(event):
    hmm = await eor(event, "`Fetching Gbanned users...`")
    gbanned_users = all_gbanned()
    GBANNED_LIST = "**Gbanned Users :**\n"
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            hel = user.chat_id
            dominator = int(hel)
            try:
                tity = await event.client.get_entity(dominator)
                name = tity.first_name
            except ValueError:
                name = "User"
            GBANNED_LIST += f"📍 [{name}](tg://user?id={dominator}) (`{dominator}`)\n"
    else:
        GBANNED_LIST = "No Gbanned Users!!"
    await hmm.edit(GBANNED_LIST)


@H1.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
        if is_gbanned(str(user.id)):
            if chat.admin_rights:
                try:
                    await H1.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                except BaseException:
                    pass
            else:
                gban_watcher += f"Reported to @admins"
            await event.reply(gban_watcher)

if H2:
    @H2.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H2.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)

if H3:
    @H3.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H3.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)

if H4:
    @H4.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H4.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)

if H5:
    @H5.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H5.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)


@dominator_cmd(pattern="gkick(?:\s|$)([\s\S]*)")
async def gkick(event):
    cid = await client_id(event)
    ForGo10God, DOMINATOR_USER, dominator_mention = cid[0], cid[1], cid[2]
    dominator = await eor(event, f"`Kicking globally ...`")
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(dominator, "`Reply to some msg or add their id.`")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(dominator, "**🥴 Nashe me hai kya lawde!!**")
    if str(userid) in DEVLIST:
        return await eod(dominator, "**😪 I'm not going to gkick my developer!!**")
    async for gkick in event.client.iter_dialogs():
        if gkick.is_group or gkick.is_channel:
            try:
                await event.client.kick_participant(gkick.id, userid)
                chats += 1
            except BaseException:
                pass

    a = gvarstat("BAN_PIC")
    pic_str = []
    if a:
        b = a.split(" ")
        for c in b:
            pic_str.append(c)
        gbpic = random.choice(pic_str)
    else:
        gbpic = cjb
    gkmsg = f"🏃 **Globally Kicked** [{name}](tg://user?id={userid})'s butts !! \n\n📝 **Chats :**  `{chats}`"
    if Config.ABUSE == "ON":
        await event.client.send_file(event.chat_id, gbpic, caption=gkmsg, reply_to=reply)
        await dominator.delete()
    else:
        await dominator.edit(gkmsg)


@dominator_cmd(pattern="gmute(?:\s|$)([\s\S]*)")
async def gm(event):
    cid = await client_id(event)
    ForGo10God, DOMINATOR_USER, dominator_mention = cid[0], cid[1], cid[2]
    dominator = await eor(event, "`Trying to gmute user...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(dominator, "**To gmute a user I'll need a userid or reply to his/her message!!**")
    name = (await event.client.get_entity(userid)).first_name
    reply = await event.get_reply_message()
    if gsql.is_gmuted(userid, "gmute"):
        return await eod(dominator, "This kid is already Gmuted.")
    if str(userid) in DEVLIST:
        return await eod(dominator, "**Sorry I'm not going to gmute them..**")
    try:
        gsql.gmute(userid, "gmute")
        if Config.ABUSE == "ON":
            await event.client.send_file(event.chat_id, shhh, caption=f"**(~‾▿‾)~ Chup [Madarchod](tg://user?id={userid}) ....**", reply_to=reply)
            await dominator.delete()
        else:
            await eor(dominator, f"**Globally Muted [{name}](tg://user?id={userid}) !!**\n\n__Kid struggling to speak__ ♪～(´ε｀ )")
    except Exception as e:
        await eod(dominator, "Error occured!\nError is " + str(e))


@dominator_cmd(pattern="ungmute(?:\s|$)([\s\S]*)")
async def endgmute(event):
    dominator = await eor(event, "`Trying to ungmute !!`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(dominator, "**To ungmute a user I'll need a userid or reply to his/her message!!**")
    name = (await event.client.get_entity(userid)).first_name
    reply = await event.get_reply_message()
    if not gsql.is_gmuted(userid, "gmute"):
        return await eod(dominator, "I don't remember I gmuted him/her...")
    try:
        gsql.ungmute(userid, "gmute")
        await eor(dominator, f"**Unmuted [{name}](tg://user?id={userid}) Globally !!**")
    except Exception as e:
        await eod(dominator, "Error occured!\nError is " + str(e))


@dominator_handler()
async def watcher(event):
    if gsql.is_gmuted(event.sender_id, "gmute"):
        await event.delete()


CmdHelp("globals").add_command(
  "gban", "<reply>/<userid>", "Globally Bans the mentioned user in 'X' chats you are admin with ban permission."
).add_command(
  "ungban", "<reply>/<userid>", "Globally Unbans the user in 'X' chats you are admin!"
).add_command(
  "listgban", None, "Gives the list of all GBanned Users."
).add_command(
  "gkick", "<reply>/<userid>", "Globally Kicks the user in 'X' chats you are admin!"
).add_command(
  "gmute", "<reply> or <userid>", "Globally Mutes the User."
).add_command(
  "ungmute", "<reply> or <userid>", "Globally Unmutes the gmutes user."
).add_command(
  "gpro", "<reply> or <username>", "Globally Promotes the mentioned user in all the chats you are admin with Add Admins permission."
).add_command(
  "gdem", "<reply> or <username>", "Globally Demotes the mentioned user in all the chats you have rights to demoted that user."
).add_info(
  "Global Admin Tool."
).add_warning(
  "✅ Harmlesss Module."
).add()
