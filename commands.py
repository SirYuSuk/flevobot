import importlib


class Commands:
    cmds = {}


    def add(self, func):
        self.cmds[func.__name__] = Command(func)


    def rm(self, name):
        del self.cmds[name]

    
    def run(self, name, bot, update):
        self.cmds[name].func(bot, update)


    def load_ext(self, path):
        ext_cmds = getattr(importlib.import_module(path), "cmds")
        for cmd in ext_cmds:
            self.add(cmd)


class Command:
    def __init__(self, func):
        self.name = func.__name__
        self.func = func
        self.help = func.__doc__        