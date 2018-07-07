from commands import Commands
import re
import telegram
from telegram.ext import RegexHandler
from telegram.ext import Updater
import yaml


# config file
try:
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
except FileNotFoundError:
    print("Configuratiebestand (config.yaml) niet aanwezig")
    exit(1)


# set prefixes
prefixes = ""
for pre in config['prefix']:
    prefixes += pre
    if pre != config['prefix'][-1]:
        prefixes += "|"


# commands
cmds = Commands()

def test(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="test")


cmds.add("test", test)


def command(bot, update):
    cmd_match = re.search(r"(" + prefixes + ")([^\s]*)(( )(.*)|)", update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=cmd_match[2])
    cmds.run(cmd_match[2], bot, update)


# initialize bot
updater = Updater(token=config['token'])
botinfo = updater.bot.get_me()
print(f"Bot: {botinfo['first_name']}\nID: {botinfo['id']}")
dispatcher = updater.dispatcher
command_handler = RegexHandler(r"(>|f/|f!)(.*)", command)
dispatcher.add_handler(command_handler)


def main():
    print(config)
    #v = 1


if __name__ == "__main__":
    main()
    updater.start_polling()
    updater.idle()