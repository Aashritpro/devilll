import asyncio
import math
import os
import heroku3
import requests
import urllib3
import sys
from os import execl
from time import sleep

from . import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
lg_id = Config.LOGGER_ID



async def restart(event):
    if HEROKU_APP_NAME and HEROKU_API_KEY:
        try:
            Heroku
        except BaseException:
            return await eor(
                event, "`HEROKU_API_KEY` is wrong. Re-Check in config vars."
            )
            await event.edit("Restarting **[ ░░░░░░░░░░░]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ █░░░░░░░░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ██░░░░░░░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ███░░░░░░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ████░░░░░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ █████░░░░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ██████░░░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ███████░░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ████████░░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ █████████░░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ██████████░ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarting **[ ███████████ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await event.edit("Restarted **[ ✓ ]** ...\nType `.ping` or `.help` to check if I am working 🙂")
    await eor(event, f"✅ **Restarted Dynos** \n**Type** `{hl}ping` **after 1 minute to check if I am working !**")
        app = Heroku.apps()[HEROKU_APP_NAME]
        app.restart()
    else:
        execl(executable, executable, "bash", "D3vilBot")


@bot.on(d3vil_cmd(pattern="restart$"))
@bot.on(sudo_cmd(pattern="restart$", allow_sudo=True))
async def re(d3vil):
    if d3vil.fwd_from:
        return
    event = await eor(d3vil, "Restarting Dynos ...")
    if HEROKU_API_KEY:
        await restart(event)
    else:
        await event.edit("Please Set Your `HEROKU_API_KEY` to restart 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱")


@bot.on(d3vil_cmd(pattern="shutdown$"))
@bot.on(sudo_cmd(pattern="shutdown$", allow_sudo=True))
async def down(d3vil):
    if d3vil.fwd_from:
        return
    await eor(d3vil, "**[ ! ]** Turning off 𝔇3𝔳𝔦𝔩𝔅𝔬𝔱 Dynos... Manually turn me on later ಠ_ಠ")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@bot.on(d3vil_cmd(pattern="(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)", outgoing=True))
@bot.on(sudo_cmd(pattern="(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)", allow_sudo=True))
async def variable(d3vil):
    if d3vil.fwd_from:
        return
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await eor(d3vil, "`[HEROKU]:" "\nPlease setup your` **HEROKU_APP_NAME**")
    exe = d3vil.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        event = await eor(d3vil, "Getting Variable Info...")
        await asyncio.sleep(1.5)
        cap = "Logger me chala jaa bsdk."
        capn = "Saved in LOGGER_ID !!"
        try:
            variable = d3vil.pattern_match.group(2).split()[0]
            if variable in ("D3VILBOT_SESSION", "BOT_TOKEN", "HEROKU_API_KEY"):
                if Config.ABUSE == "ON":
                    await bot.send_file(d3vil.chat_id, cjb, caption=cap)
                    await event.delete()
                    await bot.send_message(lg_id, f"#HEROKU_VAR \n\n`{heroku_var[variable]}`")
                    return
                else:
                    await event.edit(f"**{capn}**")
                    await bot.send_message(lg_id, f"#HEROKU_VAR \n\n`{heroku_var[variable]}`")
                    return
            if variable in heroku_var:
                return await event.edit(
                    "**Heroku Var** :" f"\n\n`{variable}` = `{heroku_var[variable]}`\n"
                )
            else:
                return await event.edit(
                    "**Heroku Var** :" f"\n\n__Error:__\n-> I doubt `{variable}` exists!"
                )
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await d3vil.client.send_file(
                        d3vil.chat_id,
                        "configs.json",
                        reply_to=d3vil.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await event.edit(
                        "**Heroku Var :**\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================"
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        event = await eor(d3vil, "Setting Heroku Variable...")
        variable = d3vil.pattern_match.group(2)
        if not variable:
            return await event.edit(f"`{hl}set var <Var Name> <Value>`")
        value = d3vil.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = d3vil.pattern_match.group(2).split()[1]
            except IndexError:
                return await event.edit(f"`{hl}set var <Var Name> <Value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await event.edit(
                f"`{variable}` **successfully changed to**  ->  `{value}`"
            )
        else:
            await event.edit(
                f"`{variable}` **successfully added with value**  ->  `{value}`"
            )
        heroku_var[variable] = value
    elif exe == "del":
        event = await eor(d3vil, "Getting info to delete Variable")
        try:
            variable = d3vil.pattern_match.group(2).split()[0]
        except IndexError:
            return await event.edit("`Please specify ConfigVars you want to delete`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await event.edit(f"**Successfully Deleted** \n`{variable}`")
            del heroku_var[variable]
        else:
            return await event.edit(f"`{variable}`  **does not exists**")


@bot.on(d3vil_cmd(pattern="usage(?: |$)", outgoing=True))
@bot.on(sudo_cmd(pattern="usage(?: |$)", allow_sudo=True))
async def dyno_usage(d3vil):
    if d3vil.fwd_from:
        return
    event = await edit_or_reply(d3vil, "`Processing...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await event.edit(
            "`Error: something bad happened`\n\n" f">.`{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await event.edit(
        "✘ **Dyno Usage** ✘:\n\n"
        f" ➠ __Dyno usage for__ • **{Config.HEROKU_APP_NAME}** • :\n"
        f"     ★  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  `{AppPercentage}`**%**"
        "\n\n"
        " ➠ __Dyno hours remaining this month__ :\n"
        f"     ★  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  `{percentage}`**%**"
        f"\n\n**Owner :** {d3vil_mention}"
    )

@bot.on(d3vil_cmd(pattern="logs$"))
@bot.on(sudo_cmd(pattern="logs$", allow_sudo=True))
async def _(dyno):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        return await eor(dyno, f"Make Sure Your HEROKU_APP_NAME & HEROKU_API_KEY are filled correct. Visit {d3vil_grp} for help.", link_preview=False)
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await dyno.reply(f"Make Sure Your Heroku AppName & API Key are filled correct. Visit {d3vil_grp} for help.", link_preview=False)
   # event = await eor(dyno, "Downloading Logs...")
    d3vil_data = app.get_log()
    await eor(dyno, d3vil_data, deflink=True, linktext=f"**🗒️ Heroku Logs of 💯 lines. 🗒️**\n\n🌟 **Bot Of :**  {d3vil_mention}\n\n🚀** Pasted**  ")
    

def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""
    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)



CmdHelp("power").add_command(
  "restart", None, "𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝗌 𝗒𝗈𝗎𝗋 𝗎𝗌𝖾𝗋𝖻𝗈𝗍. 𝖱𝖾𝖽𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖡𝗈𝗍 𝗆𝖺𝗒 𝗋𝖾𝗌𝗎𝗅𝗍 in 𝖻𝖾𝗍𝗍𝖾𝗋 𝖿𝗎𝗇𝖼𝗍𝗂𝗈𝗇𝗂𝗇𝗀 𝗈𝖿 𝖻𝗈𝗍 𝗐𝗁𝖾𝗇 𝗂𝗍𝗌 𝗅𝖺𝗀𝗀𝗒"
).add_command(
  "shutdown", None, "𝖳𝗎𝗋𝗇𝗌 𝗈𝖿𝖿 𝖣𝗒𝗇𝗈𝗌 𝗈𝖿 𝖴𝗌𝖾𝗋𝖻𝗈𝗍. 𝖴𝗌𝖾𝗋𝖻𝗈𝗍 𝗐𝗂𝗅𝗅 𝗌𝗍𝗈𝗉 𝗐𝗈𝗋𝗄𝗂𝗇𝗀 𝗎𝗇𝗅𝖾𝗌𝗌 𝗒𝗈𝗎 𝗆𝖺𝗇𝗎𝖺𝗅𝗅𝗒 𝗍𝗎𝗋𝗇 𝗂𝗍 𝗈𝗇 𝖿𝗋𝗈𝗆 𝗁𝖾𝗋𝗈𝗄𝗎"
).add_info(
  "Power Switch For Bot"
).add()

CmdHelp("heroku").add_command(
  "usage", None, "𝖢𝗁𝖾𝖼𝗄 𝗒𝗈𝗎𝗋 𝗁𝖾𝗋𝗈𝗄𝗎 𝖽𝗒𝗇𝗈 𝗁𝗈𝗎𝗋𝗌 𝗌𝗍𝖺𝗍𝗎𝗌."
).add_command(
  "set var", "<Var Name> <value>", "𝖠𝖽𝖽 𝗇𝖾𝗐 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝗈𝗋 𝗎𝗉𝖽𝖺𝗍𝖾 𝖾𝗑𝗂𝗌𝗍𝗂𝗇𝗀 𝗏𝖺𝗅𝗎𝖾/𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾\𝗇𝖠𝖿𝗍𝖾𝗋 𝗌𝖾𝗍𝗍𝗂𝗇𝗀 𝖺 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝖻𝗈𝗍 𝗐𝗂𝗅𝗅 𝗋𝖾𝗌𝗍𝖺𝗋𝗍 𝗌𝗈 𝗌𝗍𝖺𝗒 𝖼𝖺𝗅𝗆 𝖿𝗈𝗋 1 𝗆𝗂𝗇𝗎𝗍𝖾."
).add_command(
  "get var", "<Var Name", "𝖦𝖾𝗍𝗌 𝗍𝗁𝖾 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 and 𝗂𝗍𝗌 𝗏𝖺𝗅𝗎𝖾 (𝗂𝖿 𝖺𝗇𝗒) 𝖿𝗋𝗈𝗆 𝗁𝖾𝗋𝗈𝗄𝗎."
).add_command(
  "del var", "<Var Name", "Deletes the variable from heroku. Bot will restart after deleting the variable. So be calm for a minute 😃"
).add_command(
  "logs", None, "𝖦𝖾𝗍𝗌 𝗍𝗁𝖾 𝖺𝗉𝗉 𝗅𝗈𝗀 𝗈𝖿 100 𝗅𝗂𝗇𝖾𝗌 𝗈𝖿 𝗒𝗈𝗎𝗋 𝖻𝗈𝗍 𝖽𝗂𝗋𝖾𝖼𝗍𝗅𝗒 𝖿𝗋𝗈𝗆 𝗁𝖾𝗋𝗈𝗄𝗎."
).add()
