import importlib


class Commands:
    cmds = {}

    def add(self, name, func):
        self.cmds[name] = func


    def rm(self, name):
        del self.cmds[name]

    
    def run(self, name, bot, update):
        self.cmds[name](bot, update)


    def load_ext(self, path):
        ext_cmds = getattr(importlib.import_module(path), "cmds")
        for cmd in ext_cmds:
            self.add(cmd.__name__, cmd)
        