from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
from uuid import uuid4
from telegram import InlineQueryResultCachedPhoto, InlineKeyboardMarkup, InlineKeyboardButton
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_photo_date(elem):
    return elem['date']
def list_serach(lst1,lst2):
    for data in lst1:
        if data in lst2:
            return True
    return False
class bot_updater(Updater):
    def add_handler(self,handler):
        return self.dispatcher.add_handler(handler)
