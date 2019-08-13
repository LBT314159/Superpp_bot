from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
from uuid import uuid4
from telegram import InlineQueryResultCachedPhoto, InlineKeyboardMarkup, InlineKeyboardButton
import time

# 輸出Debug資訊，若要關閉把下面兩行刪除即可
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_photo_date(elem):
    return elem['date']
def list_serach(lst1,lst2):
    for data in lst1:
        if data in lst2:
            return True
    return False
class TelegramAPI:
    def __init__(self,token):
        self.updater = Updater(token)
    def SendMessage(self,bot,uid,message,markup = None):
        return bot.sendMessage(uid,message,reply_markup=markup)
    def AddHandler(self,handler):
        return self.updater.dispatcher.add_handler(handler)
    def AddHandlerFromList(self,handler_list):
        for handler in handler_list:
            self.AddHandler(handler)
    def startRunning(self):
        print('Server start')
        self.updater.start_polling()
        self.updater.idle()
