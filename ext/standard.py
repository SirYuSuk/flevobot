class Standard:
    def __init__(self, bot, config):
        self.cmd_list = [self.ma, self.ping, self.test]
        self.bot = bot
        self.config = config


    def ma(self, update, args):
        """Some test for multiple arguments"""
        for arg in args:
            self.bot.send_message(chat_id=update.message.chat_id, text=arg)


    def ping(self, update):
        """pong"""
        print(update.message.date)


    def test(self, update):
        """Some stupid test function"""
        self.bot.send_message(chat_id=update.message.chat_id, text="test")


def setup(bot, config):
    return Standard(bot, config)