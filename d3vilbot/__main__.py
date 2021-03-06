import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest

from d3vilbot import LOGS, bot, tbot
from d3vilbot.config import Config
from d3vilbot.utils import load_module, start_assistant, load_addons
from d3vilbot.version import __d3vil__ as d3vilver
hl = Config.HANDLER
D3VIL_PIC = Config.ALIVE_PIC or "https://telegra.ph/file/5abfcff75e1930dcdfaf3.mp4"

LOAD_USERBOT = os.environ.get("LOAD_USERBOT", True)
LOAD_ASSISTANT = os.environ.get("LOAD_ASSISTANT", True)    

# let's get the bot ready
async def d3vil_bot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"D3VILBOT_SESSION - {str(e)}")
        sys.exit()


# Userbot starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = TelegramClient(
                "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
            ).start(bot_token=Config.BOT_TOKEN)
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("ΰΌπππ°πππΈπ½πΆ πππ΄ππ±πΎπΰΌ")
            bot.loop.run_until_complete(d3vil_bot(Config.BOT_USERNAME))
            LOGS.info("β΅π³3ππΈπ»π±πΎπ πππ°ππππΏ π²πΎπΌπΏπ»π΄ππ΄π³β΅")
        else:
            bot.start()
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()

# imports plugins...
path = "d3vilbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

# Assistant.....
assistant = os.environ.get("ASSISTANT", None)
async def assistants():
    if assistant == "ON":
        path = "d3vilbot/assistant/*.py"
        files = glob.glob(path)
        for name in files:
            with open(name) as f:
                path1 = Path(f.name)
                shortname = path1.stem
                start_assistant(shortname.replace(".py", ""))


bot.loop.run_until_complete(assistants())

# Extra Modules...
addon = os.environ.get("EXTRA_REPO", None)             
async def addons():
    if addon == "True":
        extra_repo = "https://github.com/TEAM-D3VIL/D3VILADDONS"
        try:
            os.system(f"git clone {extra_repo}")  
        except BaseException:
            pass
        import glob
        LOGS.info("π±Loading Extra Pluginπ±")
        path = "D3VILADDONS/*.py"
        files = glob.glob(path)
        for name in files:
            with open(name) as ex:
                path2 = Path(ex.name)
                shortname = path2.stem
                try:
                    load_addons(shortname.replace(".py", ""))
                    if not shortname.startswith("__") or shortname.startswith("_"):
                        LOGS.info(f"[D3VIL-BOT 2.0] - Addons -  βInstalledβ - {shortname}")
                except Exception as e:
                    LOGS.warning(f"[D3VIL-BOT 2.0] - Addons - β οΈβ‘ERRORβ‘β οΈ - {shortname}")
                    LOGS.warning(str(e))
    else:
        print("Addons Not Loading")

bot.loop.run_until_complete(addons())

# let the party begin...
LOGS.info("βͺπππ°πππΈπ½πΆ π±πΎπ πΌπΎπ³π΄")
tbot.start()
LOGS.info("ββββββββββββββββββββ")
LOGS.info(
    "π§πΎπΊπ½ ππ @D3VIL_SUPPORT πΏππ π΄ππΊπ½ππΎ π­πΎπ. π πππ ππππ πΌππΊπππΎπ to ππΎπ πππ½πΊππΎ ππΎππΊππ½πππ ππ π£3ππππ‘ππ."
)
LOGS.info("ββββββββββββββββββββ")

# that's life...
async def d3vil_is_on():
    try:
        if Config.LOGGER_ID != 0:
            await bot.send_file(
                Config.LOGGER_ID,
                D3VIL_PIC,
                caption=f"ΚΙΙ’ΙΥΌΙaΚΚ α΄? α΄3α΄ ΙͺΚΚα΄α΄\n\n**ππ΄πππΈπΎπ½ βͺ {d3vilver}**\n\nππ²π©π `{hl}ping` or `{hl}alive` π­π¨ ππ‘πππ€! \n\nJoin [π‘3π³π¦π©π²π°π’π―ππ¬π±](t.me/D3VIL_SUPPORT) for Updates & [π3π³π¦π©π²π°π’π―ππ¬π± π π₯ππ±](t.me/D3VIL_BOT_SUPPORT) ππ¨π« ππ§π² πͺπ?ππ«π² π«ππ ππ«ππ’π§π  π‘3π³π¦π©ππ¬π±",
            )
    except Exception as e:
        LOGS.info(str(e))


    try:
        await bot(JoinChannelRequest("@D3VIL_BOT_SUPPORT"))
    except BaseException:
        pass


bot.loop.create_task(d3vil_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()


