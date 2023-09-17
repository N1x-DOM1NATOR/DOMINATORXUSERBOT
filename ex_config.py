# EDIT THIS FILE AND RENAME TO config.py TO MAKE THIS BOT WORKING
# FILL THESE VALUES ACCORDINGLY.

from DominatorBot.config.dominator_config import Config

class Development(Config):
  # get these values from my.telegram.org. 
  APP_ID = 6 # 6 is a placeholder. Fill your 6 digit api id
  API_HASH = "bf2301e561c70e59b164906e09c4bab8"   # replace this with your api hash

  # create any PostgreSQL database.
  # I recommend to use elephantsql and paste that link here
  DB_URI = ""

  # After cloning the repo and installing requirements...
  # Do `python string.py` and fill the on screen prompts.
  # String session will be saved in your saved message of telegram.
  # Put that string here.
  DOMINATORBOT_SESSION = ""

  # Create a bot in @BotFather
  # And fill the following values with bot token and username.
  BOT_TOKEN = "" #token

  # Custom Command Handler. 
  HANDLER = "."

  # Custom Command Handler for sudo users.
  SUDO_HANDLER = "!"


# end of required config
# bot
