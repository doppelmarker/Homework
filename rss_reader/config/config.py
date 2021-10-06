from rss_reader.argument_parser import ArgParser


class ConfigError(Exception):
    pass


class Config:
    def __init__(self):
        self.source = None
        self.limit = None
        self.json = None
        self.verbose = None

    def load(self, args):
        self.source = args.source
        self.limit = args.limit
        self.json = args.json
        self.verbose = args.verbose


_arg_parser = ArgParser()

config = Config()
config.load(_arg_parser.args)
