import importlib


class Commands:
    def __init__(self, bot, config):
        self.cmds = []
        self.bot = bot
        self.config = config
    

    def add(self, func):
        self.cmds.append(Command(func))


    def rm(self, name):
        self.cmds.remove(self.get_cmd(name))

    
    def run(self, name, bot, update, args):
        if len(args) == 0:
            try:
                self.get_cmd(name).func(update)
            except TypeError:
                bot.send_message(chat_id=update.message.chat_id, text=f"Too few arguments for command: `{name}`", parse_mode="Markdown")
        else:
            try:
                self.get_cmd(name).func(update, args)
            except TypeError:
                bot.send_message(chat_id=update.message.chat_id, text=f"Too many arguments for command: `{name}`", parse_mode="Markdown")


    def load_ext(self, path, update=None):
        try:
            setup = getattr(importlib.import_module(path), "setup")
        except (AttributeError, ModuleNotFoundError):
            self.bot.send_message(chat_id=update.message.chat_id, text="Invalid extension")
            return
        ext = setup(self.bot, self.config)
        for cmd in ext.cmd_list:
            self.add(cmd)

    def unload_ext(self, path):
        for cmd in self.get_ext_cmds(path):
            self.rm(cmd.name)

    
    def get_cmd(self, name):
        return list(filter(lambda x: x.name == name, self.cmds))[0]


    def get_ext_cmds(self, ext):
        return list(filter(lambda x: x.ext == ext, self.cmds))


class Command:
    def __init__(self, func):
        self.name = func.__name__
        self.func = func
        self.help = func.__doc__
        self.ext = func.__module__