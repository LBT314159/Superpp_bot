from telegram.ext import Updater, CommandHandler, MessageHandler,Filters,CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import monpa
userinPut = ['OwO']
def check(sentence):
    checkJoken =['Na','PER','LOC','VH','VD','VE','VCL','VB','VK','A']
    unused_line = monpa.pseg(str(sentence)) 
    # x for x in unused_line => 拜訪整個unused_line
    # if x[1] in checkJoken => 判斷式
    result = [x[0]  for x in unused_line if x[1] in checkJoken]
    return result

def create_button(tags,uid,fid):
    keyboard = []
    for i in tags:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])# $id$fid
    keyboard.append([InlineKeyboardButton('確認送出', callback_data='${}${}'.format(str(uid),str(fid)))])
    return InlineKeyboardMarkup(keyboard)
