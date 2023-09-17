from . import *

# assigning command
@dominator_cmd(pattern="hlo$")
async def hi(event):
    # command body
    await eor(event, "`░█─░█ █▀▀ █── █── █▀▀█ \n░█▀▀█ █▀▀ █── █── █──█ \n░█─░█ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ \n`")


# to display in help menu
CmdHelp("hlo").add_command(
  "hlo", None, "Try and see"
).add()