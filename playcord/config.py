import configparser

class Configuration:
    config = configparser.ConfigParser()
    """
    Provides an interface for storing user data.
    """
    def __init__(self, config_name : str = "playcord.ini") -> None:
        self.config_name = config_name
        self.load()

    def __getitem__(self, key):
        if key not in self.config.sections():
            self.config[key] = {}
        return self.config[key]

    def load(self):
        self.config.read(self.config_name)

    def save(self):
        with open(self.config_name, 'w+') as configfile:
            self.config.write(configfile)
