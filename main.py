import logging
import re
import telegram
import yaml
from commands import Commands
from ctx import CTX
from checks import Checks
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
from telegram.ext import Updater
from telegram.ext.dispatcher import run_async


# --- Enable logging ---
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# --- Load config file ---
try:
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
except FileNotFoundError:
    print("Configuratiebestand (config.yaml) niet aanwezig")
    exit(1)


# --- Initialize bot ---
updater = Updater(token=config['token'])
bot = updater.bot


# --- Set prefixes ---
prefixes = ""
for pre in config['prefix']:
    prefixes += pre
    if pre != config['prefix'][-1]:
        prefixes += "|"


# --- Initialize command logic ---
cmds = Commands(bot, config)
try:
    for ext in config['extension']:
        cmds.load_ext(ext)
except TypeError:
    print("No extensions present in config")


def get_arguments(message):
    cmd_match = re.search(r"(" + prefixes + r")([^\s]+)(( )(.+)|)", message)
    try:
        return cmd_match[5].split(" ")
    except AttributeError:
        return []


def is_owner(update):
    if update.message.from_user.id == config['owner']:
        return True
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Niet toegestaan")
        return False


# --- Built-in commands ---
# help command
def help(ctx):
    """Toont dit bericht"""
    global cmds
    global bot
    help_msg = ""
    if ctx.args != None:
        try:
            cmd = cmds.get_cmd(ctx.args[0].lower())
            help_msg = f"`{cmd.name}`: {cmd.help}"
        except IndexError:
            help_msg = f"Command `{ctx.args[0]}` not found!"
    else:
        help_msg += "*De volgende commando's zijn beschikbaar:*\n"
        for cmd in sorted(cmds.cmds, key=lambda x: x.name):
            help_msg += f"`{cmd.name}`: {cmd.help}\n"
    ctx.bot.send_message(chat_id=ctx.update.message.chat_id, text=help_msg, parse_mode="Markdown")


# load command
def load(ctx):
    """Laadt een nieuwe extensie"""
    if not is_owner(ctx.update):
        return
    global cmds
    cmds.load_ext(ctx.args[0], ctx.update)


# unload command
def unload(ctx):
    """Ontkoppelt een gegeven extensie"""
    if not is_owner(ctx.update):
        return
    global cmds

    cmds.unload_ext(ctx.args[0])


cmds.add(help)
cmds.add(load)
cmds.add(unload)


# --- Handler callback ---
@run_async
def command(bot, update):
    cmd_match = re.search(r"(" + prefixes + r")([^\s]+)(( )(.+)|)", update.message.text)
    args = get_arguments(update.message.text)
    if len(args) == 0:
        cmds.run(cmd_match[2], CTX(bot, config, Checks(bot), update, None))
    else:
        cmds.run(cmd_match[2], CTX(bot, config, Checks(bot), update, get_arguments(update.message.text)))



def new_title(bot, update):
    with open("names.txt", "a") as myfile:
        myfile.write(f"\n{update.message.chat_id}: {update.message.new_chat_title}")




# --- Finish initializing bot ---
botinfo = updater.bot.get_me()
print(f"Bot: {botinfo['first_name']}\nID: {botinfo['id']}")
dispatcher = updater.dispatcher
dispatcher.add_handler(RegexHandler(r"(" + prefixes + r")(.+)", command))
dispatcher.add_handler(MessageHandler(telegram.ext.Filters.status_update.new_chat_title, new_title))



if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
