from bot import Tag, Photos, InlineHandler, Bot, ButtonManager
from tgAPI import *
from database import Database
from configparser import ConfigParser
if __name__ == "__main__":
    # 從config.ini讀取token
    config          =   ConfigParser()
    config.read('config.ini')
    token           =   config.get('default','Token')

    tg              =   TelegramAPI(token)
    db              =   Database()              # 用來處理資料儲存相關
    button_mgr      =   ButtonManager(db,tg)    #處理按鈕的新增和修改
    tag_proc        =   Tag(db,tg,button_mgr)   # 用來Tag新增/修改
    photo_proc      =   Photos(db,tg)           # 用來加入圖片
    inline_handler  =   InlineHandler(db,tg)    # 用來處理inline查詢請求(叫出圖片)
    bot             =   Bot(db,tg)              # 處理當前模式的切換
    # 用一個LIST儲存Handlers之後再一一加入
    handlers        =  [CommandHandler('cancel',bot.cancel_mode),
                        CommandHandler('add',bot.add_mode),
                        CommandHandler('start',bot.start_command),
                        CommandHandler('tag',bot.tag_change_command),
                        MessageHandler(Filters.photo,photo_proc.AddPhoto),
                        MessageHandler(Filters.text,tag_proc.HandleMessageQuery),
                        InlineQueryHandler(inline_handler.InlineQuery),
                        CallbackQueryHandler(button_mgr.ButtonCallback)
                        ]
    tg.AddHandlerFromList(handlers) # 從List加入handler

    tg.startRunning()
    db.SaveAll()   # 在Server關閉前儲存資料
    print('Server idle')