import importlib


class Commands:
    cmds = []
    

    def add(self, func):
        self.cmds.append(Command(func))


    def rm(self, name):
        self.cmds.remove(self.get_cmd(name))

    
    def run(self, name, bot, update, args):
        if len(args) == 0:
            try:
                self.get_cmd(name).func(bot, update)
            except TypeError:
                bot.send_message(chat_id=update.message.chat_id, text=f"Too few arguments for command: `{name}`", parse_mode="Markdown")
        else:
            try:
                self.get_cmd(name).func(bot, update, args)
            except TypeError:
                bot.send_message(chat_id=update.message.chat_id, text=f"Too many arguments for command: `{name}`", parse_mode="Markdown")


    def load_ext(self, path):
        ext_cmds = getattr(importlib.import_module(path), "cmd_list")
        for cmd in ext_cmds:
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