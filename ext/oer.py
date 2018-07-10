class Oer:
    def __init__(self, bot, config):
        self.cmd_list = [self.oer]
        self.bot = bot
        self.config = config

    
    def oer(self, update, args=None):
        pass


def setup(bot, config):
    return Oer(bot, config)