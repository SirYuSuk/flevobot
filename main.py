import telegram
import yaml


# config file
try:
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
except FileNotFoundError:
    print("Configuratiebestand (config.yaml) niet aanwezig")
    exit(1)


# initialize bot
bot = telegram.Bot(token=config['token'])
botinfo = bot.get_me()
print(f"Bot: {botinfo['first_name']}\nID: {botinfo['id']}")


def main():
    #print(config)
    v = 1


if __name__ == "__main__":
    main()