import logging
import re
import telegram
import yaml
from commands import Commands
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


# --- Set prefixes ---
prefixes = ""
for pre in config['prefix']:
    prefixes += pre
    if pre != config['prefix'][-1]:
        prefixes += "|"


# --- Initialize command logic ---
cmds = Commands()
for ext in config['extension']:
    cmds.load_ext(ext)


def command(bot, update):
    cmd_match = re.search(r"(" + prefixes + r")([^\s]+)(( )(.+)|)", update.message.text)
    cmds.run(cmd_match[2], bot, update, get_arguments(update.message.text))

def get_arguments(message):
    cmd_match = re.search(r"(" + prefixes + r")([^\s]+)(( )(.+)|)", message)
    try:
        return cmd_match[5].split(" ")
    except AttributeError:
        return []


# --- Built-in commands ---
# help command
def help(bot, update, args=None):
    """Sends this message"""
    global cmds
    help_msg = ""
    if args != None:
        try:
            cmd = cmds.get_cmd(args[0])
            help_msg = f"*{cmd.name}*: `{cmd.help}`"
        except IndexError:
            help_msg = f"Command: `{args[0]}` not found!"
    else:
        for cmd in sorted(cmds.cmds, key=lambda x: x.name):
            help_msg += f"*{cmd.name}*: `{cmd.help}`\n"
    bot.send_message(chat_id=update.message.chat_id, text=help_msg, parse_mode="Markdown")


# load command
def load(bot, update):
    """Loads a new extension"""
    global cmds
    cmds.load_ext(get_arguments(update.message.text))


# unload command
def unload(bot, update):
    """Unloads a given extension"""
    global cmds
    cmds.unload_ext(get_arguments(update.message.text))


cmds.add(help)
cmds.add(load)
cmds.add(unload)


# --- Initialize bot ---
updater = Updater(token=config['token'])
botinfo = updater.bot.get_me()
print(f"Bot: {botinfo['first_name']}\nID: {botinfo['id']}")
dispatcher = updater.dispatcher
command_handler = RegexHandler(r"(" + prefixes + r")(.+)", command)
dispatcher.add_handler(command_handler)



if __name__ == "__main__":
    updater.start_polling()
    updater.idle()