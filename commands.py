class Commands:
    cmds = {}

    def add(self, name, func):
        self.cmds[name] = func


    def rm(self, name):
        del self.cmds[name]

    
    def run(self, name, bot, update):
        self.cmds[name](bot, update)
        