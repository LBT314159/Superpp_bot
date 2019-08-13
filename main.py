from bot import Bot_body
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
if __name__ == "__main__":
    token = config.get('default','Token')
    my_bot = Bot_body(token)
    my_bot.start()