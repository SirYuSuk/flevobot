import logging
import re
import telegram
import yaml
from commands import Commands
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
from telegram.ext import Updater


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
        bot.send_message(chat_id=update.message.chat_id, text="Insufficient permissions")
        return False


# --- Built-in commands ---
# help command
def help(update, args=None):
    """Sends this message"""
    global cmds
    global bot
    help_msg = ""
    if args != None:
        try:
            cmd = cmds.get_cmd(args[0].lower())
            help_msg = f"*{cmd.name}*: `{cmd.help}`"
        except IndexError:
            help_msg = f"Command `{args[0]}` not found!"
    else:
        for cmd in sorted(cmds.cmds, key=lambda x: x.name):
            help_msg += f"*{cmd.name}*: `{cmd.help}`\n"
    bot.send_message(chat_id=update.message.chat_id, text=help_msg, parse_mode="Markdown")


# load command
def load(update, args):
    """Loads a new extension"""
    if not is_owner(update):
        return
    global cmds
    cmds.load_ext(args[0], update)


# unload command
def unload(update, args):
    """Unloads a given extension"""
    if not is_owner(update):
        return
    global cmds
    
    cmds.unload_ext(args[0])


cmds.add(help)
cmds.add(load)
cmds.add(unload)


# --- Handler callback ---
def command(bot, update):
    cmd_match = re.search(r"(" + prefixes + r")([^\s]+)(( )(.+)|)", update.message.text)
    cmds.run(cmd_match[2], bot, update, get_arguments(update.message.text))


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