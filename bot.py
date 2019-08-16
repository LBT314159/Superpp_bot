from tgAPI import *
from sentencecut import check
#處理按鈕的新增和修改
class ButtonManager:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
    def creatButtonsFromTags(self, user_id, photo_id, tags):
        keyboard = [[]]
        for tag in tags:
            keyboard[0].append(InlineKeyboardButton(tag, callback_data='${}${}'.format(photo_id,tag)))
        return InlineKeyboardMarkup(keyboard)
    def ButtonCallback(self, bot, update):
        callback_query  =   update.callback_query
        callback_data   =   callback_query.data
        callback_data   =   callback_data.split('$')[1:]
        photo_id        =   callback_data[0]
        query_text      =   callback_data[1]
        user_id = update.callback_query.from_user.id
        current_photo_tags  =   self.db.getPhotoTags(user_id, photo_id)
        if query_text in current_photo_tags:
            current_photo_tags.remove(query_text)
            bot.sendMessage(user_id,'已為圖片{}移除標籤:{}'.format(photo_id,query_text))
        else:
            current_photo_tags.append(query_text)
            bot.sendMessage(user_id,'已為圖片{}加入標籤:{}'.format(photo_id,query_text))
        self.db.setPhotoTags(user_id, photo_id, current_photo_tags)
        

# 用來Tag新增/修改
class Tag:
    def __init__(self,db,telegram,button_manager):
        self.db                 =   db
        self.tg                 =   telegram
        self.creat_button_lock  =   {}
        self.reply_markup       =   {}
        self.user_temp_data     =   {}
        self.button_manager     =   button_manager
    def HandleMessageQuery(self,bot,update):
        uid = update.message.from_user.id
        if self.db.getUserMode(uid) == 'add':
            self.appendTag(bot,update)
        elif self.db.getUserMode(uid) == 'tag':
            self.editTag(bot,update)
    def appendTag(self,bot,update):
        user_id = update.message.from_user.id
        if self.db.hasNoTagPhotos(user_id):
            no_tag_photos = self.db.getNoTagPhotos(user_id)
            photo_id = no_tag_photos[0]['fid']
            if update.message.text.find('#') != -1:
                self.db.setPhotoTags(user_id,photo_id,update.message.text.split('#')[1:])
                bot.sendMessage(user_id,'好ㄉ，已為id為{}的圖片加上tag:{}'.format(str(photo_id),update.message.text))
                return
            else:
                userinPut = update.message.text.replace('\n', ' ')
                photo_tags = check(userinPut)
                reply_markup = self.button_manager.creatButtonsFromTags(user_id, photo_id, photo_tags)
                self.user_temp_data[str(user_id)] = {}
                self.user_temp_data[str(user_id)]['current_tags'] = []
                bot.sendMessage(user_id,'點擊按鈕即可為圖片{}加入標籤(再次點擊即可移除)'.format(photo_id), reply_markup=reply_markup)
                return
        else:
            bot.sendMessage(user_id,'很抱歉，目前沒有圖片是還未加上Tag的喔')
    def editTag(self,bot,update):
        uid = update.message.from_user.id
        user_input_query = update.message.text.split(':')
        photo_id = int(user_input_query[0])
        photo = self.db.getPhotoFromID(uid,photo_id)
        if photo:
                self.db.setPhotoTags(uid,photo_id,user_input_query[1].split('#')[1:])
                self.db.setUserMode(uid,'none')
                bot.sendMessage(uid,'好ㄉ，已為id為'+str(photo_id)+'的圖片加上tag:'+user_input_query[1]+'\n\n同時已離開Tag編輯模式，輸入 /tag 再次進入')
                return
        bot.sendMessage(uid,'很抱歉，找不到符合ID的圖片，請檢察您的輸入')
    
# 用來加入圖片
class Photos:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
    def AddPhoto(self,bot,update):
        user_id = update.message.from_user.id
        if self.db.getUserMode(user_id) == 'add':
            fid = self.db.appendUserPhotos(user_id, update.message.photo[0].file_id)
            if fid != -1:
                bot.sendMessage(user_id,'已加入一張圖片，id為:{}'.format(fid))
                bot.sendMessage(user_id,'接著請輸入該圖片的tag(ex:#Dog#玩球)')
                bot.sendMessage(user_id,'您也可以輸入一句符合該圖片的描述句子BOT將把該句子轉換成適合的tag供您選擇')
            else:
                bot.sendMessage(user_id,'無法加入圖片，圖片可能已經存在')
# 用來處理inline查詢請求(叫出圖片)
class InlineHandler:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
    def InlineQuery(self, bot, update):
        tags = update.inline_query.query.split(' ')
        user_id = update.inline_query.from_user.id
        results = []
        Photos  = self.db.getPhotosByTags(user_id, tags)
        for photo in Photos:
            results.append(
                InlineQueryResultCachedPhoto(id = uuid4(), photo_file_id = photo['photo'])
                )
        #update.inline_query.answer(results)
        bot.answer_inline_query(update.inline_query.id, results, is_personal = True, cache_time = 0)

# 處理當前模式的切換
class Bot:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
    def start_command(self,bot,update):
        uid = update.message.from_user.id
        if not self.db.CheckUserExist(uid):
            self.db.AddUser(uid)
        else:
            pass
        bot.sendMessage(uid,'新來的童鞋你好，歡迎使用本Bot，輸入 /add 進入新增模式，此模式下可以加入梗圖，在此模式下傳送給偶的所有圖片都會被加入資料庫，如果想離開這個模式輸入 /cancel 即可\n')
        bot.sendMessage(uid,'如果要修改標籤，輸入 /tag 即可進入標籤修改模式')
        bot.sendMessage(uid,'在聊天欄內輸入 @superpp_bot 後面加上之前加的tag即可選擇所匹配的梗圖喔!多個Tag用空格分開即可')
    def add_mode(self, bot, update):
        user_id = update.message.from_user.id
        self.db.setUserMode(user_id, 'add')
        bot.sendMessage(user_id,'已進入新增模式，傳些好料的圖片吧')
    def cancel_mode(self, bot, update):
        user_id = update.message.from_user.id
        self.db.setUserMode(user_id, 'none')
        bot.sendMessage(user_id,'離開當前模式')
    def tag_change_command(self, bot, update):
        user_id = update.message.from_user.id
        self.db.setUserMode(user_id, 'tag')
        bot.sendMessage(user_id,'已進入Tag修改模式，請輸入 <圖片ID>:<新的Tags>')